--------------------------------------------------------------------------------
-- PostgreSQL database ...
-- Author: Mikael Vind Mikkelsen
--------------------------------------------------------------------------------
INSERT INTO depth.fact_raster_cfd(
    cell_x,
    cell_y,
    division_id,
    date_id,
    cfd_gte,
    ship_type_id,
    rast
)
WITH cells AS (
    SELECT
        fd50m.cell_x,
        fd50m.cell_y,
        dc50m.geom,
        fd50m.division_id,
        max(fd50m.draught) AS max_draught,
        fd50m.ship_type_id,
        fd50m.date_id as date_id
    FROM depth.fact_depth_50m AS fd50m
    INNER JOIN public.dim_cell_50m AS dc50m
        ON fd50m.cell_x = dc50m.x
        AND fd50m.cell_y = dc50m.y
        AND fd50m.division_id = dc50m.partition_id
    WHERE fd50m.date_id = :date_key
    AND fd50m.confidence_depth_01 >= :confidence
    AND fd50m.draught IS NOT NULL
    GROUP BY cell_x, cell_y, geom, division_id, ship_type_id, date_id
),

rasters AS (
    SELECT
        ST_Union(
            ST_AsRaster(
                cells.geom,
                ST_MakeEmptyRaster(795000, 420000, 3600000, 3055000, 50, 50, 0, 0, 3034),
                '32BF'::text,
                max_draught::float
            )
        ) AS rast,
        cells.cell_x / (5000 / 50) AS cell_x,
        cells.cell_y / (5000 / 50) AS cell_y,
        cells.division_id,
        cells.ship_type_id,
        cells.date_id,
        :confidence AS confidence

    FROM cells
    GROUP BY cells.cell_x / (5000 / 50),
             cells.cell_y / (5000 / 50),
             cells.division_id,
             cells.ship_type_id,
             cells.date_id
)

SELECT
    rasters.cell_x AS cell_x,
    rasters.cell_y AS cell_y,
    rasters.division_id AS division_id,
    rasters.date_id AS date_id,
    rasters.confidence as cfg_gte,
    rasters.ship_type_id AS ship_type_id,
    rasters.rast AS rast
FROM rasters;
