"""SQL queries for the export map module."""

# noinspection SqlNoDataSourceInspection
query_count_ship = """
WITH cells AS (
    SELECT
        fd50m.cell_x,
        fd50m.cell_y,
        dc50m.geom,
        fd50m.division_id,
        count(DISTINCT mmsi) AS cnt
    FROM depth.fact_depth_50m AS fd50m
    INNER JOIN public.dim_cell_50m AS dc50m
        ON fd50m.cell_x = dc50m.x
        AND fd50m.cell_y = dc50m.y
        AND fd50m.division_id = dc50m.partition_id
    INNER JOIN public.dim_ship as ds
        ON fd50m.ship_id = ds.ship_id

    {% if mobile_type or ship_type %}
    INNER JOIN public.dim_ship_type AS dst
        ON fd50m.ship_type_id = dst.ship_type_id
    {% endif %}

    WHERE fd50m.draught IS NOT NULL

    {% if start_date and end_date %}
    AND fd50m.date_id BETWEEN {{start_date}} AND {{end_date}}
    {% endif %}

    {% if confidence %}
    AND fd50m.confidence_depth_01 >= {{confidence}}
    {% endif %}

    {% if mobile_type %}
    AND dst.mobile_type = 'Class ' || {{mobile_type}}
    {% endif %}

    {% if enc %}
    AND st_intersects(geom,
                  (SELECT st_transform(geom, 3034)
                   FROM public.enc
                   WHERE title = {{enc}}
                   AND country = 'Denmark'))
    {% endif %}

    {% if ship_type %}
    AND dst.ship_type = {{ship_type}}
    {% endif %}

    GROUP BY cell_x, cell_y, geom, division_id
),

rasters AS (
    SELECT
        ST_Union(
            ST_AsRaster(
                cells.geom,
                ST_MakeEmptyRaster(795000, 420000, 3600000, 3055000, 50, 50, 0, 0, 3034),
                '32BF'::text,
                cnt::integer
            )
        ) AS rast,
        cells.cell_x / (5000 / 50) AS cell_x,
        cells.cell_y / (5000 / 50) AS cell_y,
        cells.division_id

    FROM cells
    GROUP BY cells.cell_x / (5000 / 50),
             cells.cell_y / (5000 / 50),
             cells.division_id
)

SELECT st_asgdalraster(st_union(rast, 'SUM'), 'GTiff', ARRAY['COMPRESS=DEFLATE', 'NUM_THREADS=ALL_CPUS']) as tiff
FROM rasters;
"""

# noinspection SqlNoDataSourceInspection
query_count_traj = """
WITH cells AS (
    SELECT
        fd50m.cell_x,
        fd50m.cell_y,
        dc50m.geom,
        fd50m.division_id,
        count(*) AS cnt
    FROM depth.fact_depth_50m AS fd50m
    INNER JOIN public.dim_cell_50m AS dc50m
        ON fd50m.cell_x = dc50m.x
        AND fd50m.cell_y = dc50m.y
        AND fd50m.division_id = dc50m.partition_id

    {% if mobile_type or ship_type %}
    INNER JOIN public.dim_ship_type AS dst
        ON fd50m.ship_type_id = dst.ship_type_id
    {% endif %}

    WHERE fd50m.draught IS NOT NULL

    {% if start_date and end_date %}
    AND fd50m.date_id BETWEEN {{start_date}} AND {{end_date}}
    {% endif %}

    {% if confidence %}
    AND fd50m.confidence_depth_01 >= {{confidence}}
    {% endif %}

    {% if mobile_type %}
    AND dst.mobile_type = 'Class ' || {{mobile_type}}
    {% endif %}

    {% if enc %}
    AND st_intersects(geom,
                  (SELECT st_transform(geom, 3034)
                   FROM public.enc
                   WHERE title = {{enc}}
                   AND country = 'Denmark'))
    {% endif %}
    
    {% if ship_type %}
    AND dst.ship_type = {{ship_type}}
    {% endif %}

    GROUP BY cell_x, cell_y, geom, division_id
),

rasters AS (
    SELECT
        ST_Union(
            ST_AsRaster(
                cells.geom,
                ST_MakeEmptyRaster(795000, 420000, 3600000, 3055000, 50, 50, 0, 0, 3034),
                '32BF'::text,
                cnt::integer
            )
        ) AS rast,
        cells.cell_x / (5000 / 50) AS cell_x,
        cells.cell_y / (5000 / 50) AS cell_y,
        cells.division_id

    FROM cells
    GROUP BY cells.cell_x / (5000 / 50),
             cells.cell_y / (5000 / 50),
             cells.division_id
)

SELECT st_asgdalraster(st_union(rast, 'SUM'), 'GTiff', ARRAY['COMPRESS=DEFLATE', 'NUM_THREADS=ALL_CPUS']) as tiff
FROM rasters;
"""

# noinspection SqlNoDataSourceInspection
query_draught_month = """
SELECT st_asgdalraster(st_union(rast, 'MAX'), 'GTiff', ARRAY['COMPRESS=DEFLATE', 'NUM_THREADS=ALL_CPUS']) as tiff
FROM (
    SELECT st_union(fr_month.rast, 'MAX') AS rast
    FROM depth.fact_raster_cfd_month AS fr_month
    
    {% if ship_type %}
    INNER JOIN public.dim_ship_type AS dst ON fr_month.ship_type_id = dst.ship_type_id
    {% endif %}
        
    WHERE TRUE

    {% if confidence %}
    AND fr_month.cfd_gte = {{confidence}}
    {% endif %}

    {% if start_month and end_month %}
    AND fr_month.month BETWEEN {{start_month}} AND {{end_month}}
    {% endif %}

    {% if start_year and end_year %}
    AND fr_month.year BETWEEN {{start_year}} AND {{end_year}}
    {% endif %}

    {% if enc %}
    AND st_intersects(rast,
                      (SELECT st_transform(geom, 3034)
                             FROM public.enc
                             WHERE title = {{enc}}
                             AND country = 'Denmark'))
    {% endif %}
    
    {% if ship_type %}
    AND dst.ship_type = {{ship_type}}
    {% endif %}

) AS fr;
"""

# TODO: Implement this query.
confidence = """
"""

if __name__ == "__main__":
    from jinjasql import JinjaSql

    j = JinjaSql(param_style='named')

    params = {
        "imo": "9442184",
        "flag_region": "europe"
    }

    sql = ("SELECT * FROM public.dim_ship "
           "WHERE imo = {{imo}} "
           "{% if flag_region %}"
           "AND flag_region = {{flag_region}}"
           "{% endif %}")

    print(j.prepare_query(sql, params))

    from dipaal.settings import get_dipaal_engine

    engine = get_dipaal_engine()

    from aau_ais_utilities.connections import PostgreSQLConnection

    connection = PostgreSQLConnection(engine)

    query, bind_params = j.prepare_query(sql, params)

    result = connection.execute_raw(sql=query, params=bind_params)

    for row in result.fetchall():
        print(row)
