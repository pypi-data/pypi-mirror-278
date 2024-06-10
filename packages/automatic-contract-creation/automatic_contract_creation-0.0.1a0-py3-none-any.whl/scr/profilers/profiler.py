import polars as pl
import polars.selectors as cs
from automatic_contract_creation.scr.connectors.connection_manager import ConnectionManager
import datetime




class Profiler(ConnectionManager):
    def define_categorical(self, lf):
        len_df= lf.select(pl.len()).collect().row(0)[0]
        cat_columns = pl.Series(
            lf.select(
                cs.by_dtype(pl.String, cs.INTEGER_DTYPES).unique().count()
            ).select(
                pl.all().map_elements(
                    lambda x: (len_df- x) / len_df, return_dtype=float)
        ).melt().filter(
                pl.col('value') > 0.95
            ).select('variable').collect()
        ).to_list()

        return cat_columns


    def compute_metrics(self, lazyframe, dt: str=None):
        lf = lazyframe.cast({pl.Decimal: pl.Float64})
        if dt: lf = lf.cast({dt: pl.Datetime})

        categorical_columns = lf.select(cs.categorical()).columns
        if len(categorical_columns) == 0: categorical_columns.extend(self.define_categorical(lf))
        numeric_columns = lf.select(cs.numeric()).columns
        temporal_columns = lf.select(cs.temporal()).columns
        string_columns = lf.select(cs.string()).columns
        bool_columns = lf.select(cs.boolean()).columns
        others = lf.select(~cs.by_name(numeric_columns,
                                            temporal_columns,
                                            categorical_columns,
                                            string_columns,
                                            bool_columns)).columns
        dt =dt or (temporal_columns[0] if temporal_columns else str(datetime.datetime.now()))


        df_info = pl.concat([
            lf.select(
                column = pl.lit('all'),
                rows = pl.len(),
                percent_dup =(
                        (pl.len() - lf.unique().with_row_index(offset=1).last().select(
                            pl.col('index')
                        ).collect())
                        /pl.len()
                )
            ),
            lf.filter(
                pl.col(dt).dt.hour().is_between(9, 23)
            ).group_by(
                pl.col(dt).dt.hour()
            ).agg(
                pl.len()
            ).select(
                quantile_05_morning = pl.col('len').quantile(0.05),
                quantile_95_morning = pl.col('len').quantile(0.95)
            ),
            lf.filter(
                ~pl.col(dt).dt.hour().is_between(9, 23)
            ).group_by(
                pl.col(dt).dt.hour()
            ).agg(
                pl.len()
            ).select(
                quantile_05_night = pl.col('len').quantile(0.05),
                quantile_95_night = pl.col('len').quantile(0.95)
            )
        ], how='horizontal').collect()



        df_describe =  pl.concat([
            lf.null_count().melt(variable_name='column',
                                 value_name='null_count'),
            lf.unique().count().melt(variable_name='column',
                                     value_name='percent_dup'),
            lf.select(pl.all().map_elements(
                lambda s: (s == 0) | (s == "0") | (s == "0.0")
                , return_dtype=bool).sum()
                       ).melt(variable_name='column',
                              value_name='percent_zeros'),
            lf.select(pl.all().map_elements(
                lambda s: s == "", return_dtype=bool).sum()
                      ).melt(variable_name='column',
                             value_name='percent_empty_strings'),
            lf.select(pl.exclude(categorical_columns).str.contains(r'^\s+$')).sum().melt(variable_name='column',
                                                                  value_name='percent_strings_with_spaces'),
            lf.select(pl.col(numeric_columns + temporal_columns).min()).cast(
                {cs.numeric(): pl.String, cs.temporal(): pl.String}
            ).melt(variable_name='column',
                   value_name='minimum'),
            lf.select(pl.col(numeric_columns + temporal_columns).max()).cast(
                {cs.numeric(): pl.String, cs.temporal(): pl.String}
            ).melt(variable_name='column',
                   value_name='maximum')
          ], how='align').with_columns(
            pl.exclude(['column', 'minimum', 'maximum']).map_elements(
                lambda x: round(x / df_info['rows'][0], 3),
                return_dtype=float
            )
        ).collect()

        distribution_percentage = pl.DataFrame()

        if len(categorical_columns)>0:
            for clm in lf.select(
                    pl.col(categorical_columns).unique().count()
            ).melt().filter(pl.col('value') < 20).collect()['variable']:
                count_perc = (lf.select(
                    pl.col(clm).value_counts(sort=True)
                ).unnest(clm).with_columns(
                    column=pl.lit(clm),
                    cat_dist=pl.col(clm),
                    percent_of_total=pl.col('count') / df_info['rows'][0]
                ).collect())

                combined_list = [
                    f"{row['cat_dist']}: {row['percent_of_total']}"
                    for row in count_perc.to_dicts()
                ]

                distribution_percentage = pl.concat([distribution_percentage,
                                                     pl.DataFrame({'column': clm, 'cat_dist': [combined_list]})
                                                     ])

        how_concat = 'align' if distribution_percentage.height>0 else 'diagonal_relaxed'
        final_df = pl.concat(
            [pl.concat(
                [
                    df_info,
                    df_describe
                ], how='diagonal'),
                distribution_percentage
            ], how=how_concat)


        return final_df

    def save_to_csv(self, lazyframe, dt: str=None):
        dt = dt if dt else None
        self.compute_metrics(lazyframe, dt).with_columns(
            pl.col('cat_dist').map_elements(
                lambda col: str(col.to_list()), return_dtype=pl.String)
        ).write_csv('report.csv')

        print(f'Report saved!')
