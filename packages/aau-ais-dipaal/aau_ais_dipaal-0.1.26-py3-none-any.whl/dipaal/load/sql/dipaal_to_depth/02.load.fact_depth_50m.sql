--------------------------------------------------------------------------------
-- PostgreSQL database insert stastement for the depth data.
-- Author: Mikael Vind Mikkelsen
-- This insert statement is used to insert data into the fact table fact_depth_50m.
-- Requirements:
    -- The existence of the following tables from the DIPAAL schema:
        -- public.dim_ship
        -- public.dim_ship_type
        -- public.fact_cell_50m
        -- public.dim_nav_status
-- The DIPAAL schema exists under the 'public' schema at the time of writing.
--------------------------------------------------------------------------------

-- Insert statement:
INSERT INTO depth.fact_depth_50m (cell_x, cell_y, division_id, ship_id, ship_type_id, trajectory_sub_id,
                                  nav_status_id, date_id, time_id, draught, SOG, COG,
                                  confidence_depth_01, confidence_depth_02, confidence_depth_03)
SELECT
    fc_50m.cell_x,
    fc_50m.cell_y,
    fc_50m.partition_id as division_id,
    ds.ship_id,
    dst.ship_type_id,
    fc_50m.trajectory_sub_id,
    fc_50m.nav_status_id,
    fc_50m.entry_date_id as date_id,
    fc_50m.entry_time_id as time_id,
    fc_50m.draught,
    NULL as SOG,
    NULL as COG,
    NULL as confidence_1,
    NULL as confidence_2,
    NULL as confidence_3
FROM
    public.dim_ship as ds,
    public.dim_ship_type as dst,
    public.fact_cell_50m as fc_50m,
    public.dim_nav_status as dns
WHERE
    -- Join conditions
    ds.ship_type_id = dst.ship_type_id
    AND fc_50m.ship_id = ds.ship_id
    AND fc_50m.nav_status_id = dns.nav_status_id
    -- Temporal conditions
    AND
    STBOX(span(
        timestamp_from_date_time_id(:start_date, :start_time),
        timestamp_from_date_time_id(:end_date, :end_time),
        True, True))
        && fc_50m.st_bounding_box
    AND
    fc_50m.entry_date_id BETWEEN :start_date AND :end_date
    AND
    fc_50m.entry_time_id BETWEEN :start_time AND :end_time;
