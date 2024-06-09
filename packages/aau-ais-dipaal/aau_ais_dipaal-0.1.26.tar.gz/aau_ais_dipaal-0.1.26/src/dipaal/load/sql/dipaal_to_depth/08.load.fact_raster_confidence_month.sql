--------------------------------------------------------------------------------
-- PostgreSQL database ...
-- Author: Mikael Vind Mikkelsen
--------------------------------------------------------------------------------
INSERT INTO depth.fact_raster_cfd_month(
    cell_x,
    cell_y,
    year,
    month,
    division_id,
    cfd_gte,
    ship_type_id,
    rast
) SELECT
    frc.cell_x,
    frc.cell_y,
    dd.year,
    dd.month_of_year as month,
    frc.division_id,
    frc.cfd_gte,
    frc.ship_type_id,
    ST_Union(frc.rast) as rast
FROM depth.fact_raster_cfd as frc
INNER JOIN public.dim_date dd ON frc.date_id = dd.date_id
WHERE frc.date_id BETWEEN :start_date AND :end_date
GROUP BY frc.cell_x, frc.cell_y, dd.year, dd.month_of_year, frc.division_id, frc.cfd_gte, frc.ship_type_id
ON CONFLICT (cell_x, cell_y, division_id, year, month, cfd_gte, ship_type_id) DO UPDATE SET rast = EXCLUDED.rast; --Temporary fix to avoid duplicate key error