--------------------------------------------------------------------------------
-- PostgreSQL procedures and call for updating confidence values.
-- Author: Mikael Vind Mikkelsen
-- These procedures and call statement, are used to update the confidence_depth_01
--  column in the fact_depth_50m table.
-- Requirements:
    -- The existence of the following table from the DIPAAL schema:
        -- public.dim_ship
    -- The existence of the following table and materialized view from the DIPAAL schema:
        -- depth.fact_depth_50m
        -- depth.mv_ship_tl_depth_profile
--------------------------------------------------------------------------------

-- Procedure (update confidence 1):
CREATE OR REPLACE PROCEDURE depth.update_confidence_depth_01(
    start_date_id integer,
    end_date_id integer
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF length(start_date_id::text) != 8 OR length(end_date_id::text) != 8 THEN
        RAISE EXCEPTION 'data id must be 8 digits long';
    END IF;

    IF start_date_id > end_date_id THEN
        RAISE EXCEPTION 'start_date_id must be lower or same as end_date_id';
    END IF;

    -- Update all confidence_depth_01 to 0, done to avoid edge cases such as draught being null and sampling
    --  from mv_ship_tl_depth_profile not catching all dimensions due to tablesample not being able to sample all rows.
    UPDATE depth.fact_depth_50m fact
    SET confidence_depth_01 = 0
    WHERE date_id BETWEEN start_date_id AND end_date_id;

    UPDATE depth.fact_depth_50m fact
    SET confidence_depth_01 = (CASE
        -- Ranges are (exclusive, inclusive]
        WHEN fact.draught > mv.q02pct_depth AND fact.draught <= mv.q05pct_depth THEN 0.5
        WHEN fact.draught > mv.q05pct_depth AND fact.draught <= mv.q10pct_depth THEN 0.7
        WHEN fact.draught > mv.q10pct_depth AND fact.draught <= mv.q90pct_depth THEN 1
        WHEN fact.draught > mv.q90pct_depth AND fact.draught <= mv.q95pct_depth THEN 0.7
        WHEN fact.draught > mv.q95pct_depth AND fact.draught <= mv.q98pct_depth THEN 0.5
        ELSE 0
        END)
    FROM
        depth.mv_ship_tl_depth_profile AS mv,
        public.dim_ship AS ds
    WHERE fact.ship_id = ds.ship_id
    AND fact.ship_type_id = ds.ship_type_id
    AND ds.ship_type_id = mv.ship_type_id
    -- [min_length, max_length)
    AND ds.length >= min_length
    AND ds.length < max_length
    AND fact.date_id BETWEEN start_date_id AND end_date_id;
END;$$;

CALL depth.update_confidence_depth_01(:start_date, :end_date);