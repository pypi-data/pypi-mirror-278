"""SQL queries for the extract cell module."""

# noinspection SqlNoDataSourceInspection
empty_query = """
SELECT EXISTS(
SELECT 1
 FROM {{grid_table | sqlsafe}} as gt
   INNER JOIN public.dim_ship AS ds ON gt.ship_id = ds.ship_id
   INNER JOIN public.dim_ship_type AS dst ON gt.ship_type_id = dst.ship_type_id
 WHERE TRUE
  AND gt.cell_x = {{cell_x}}
  AND gt.cell_y = {{cell_y}}
  AND dst.mobile_type = 'Class A'

  {% if from_date and to_date %}
  AND gt.date_id BETWEEN {{from_date}} AND {{to_date}}
  {% endif %}
  );
"""

# noinspection SqlNoDataSourceInspection
meta_query = """
SELECT 
  avg(gt.draught) as avg_draught,
  count(DISTINCT ds.mmsi) as num_ships,
  count(*) as num_trips
FROM depth.fact_depth_50m as gt
INNER JOIN public.dim_ship AS ds ON gt.ship_id = ds.ship_id
  INNER JOIN public.dim_ship_type AS dst ON gt.ship_type_id = dst.ship_type_id
WHERE TRUE
  AND cell_x = {{cell_x}}
  AND cell_y = {{cell_y}}
  AND dst.mobile_type = 'Class A'
  {% if from_date and to_date %}
  AND gt.date_id BETWEEN {{from_date}} AND {{to_date}}
  {% endif %};
"""

# noinspection SqlNoDataSourceInspection
ship_query = """
SELECT ds.mmsi,
       ds.name,
       dst.ship_type,
       count(*) as num_trips,
       min(draught) as min_draught,
       max(draught) as max_draught,
       dst.mobile_type 
FROM {{grid_table | sqlsafe}} AS gt
  INNER JOIN public.dim_ship AS ds ON gt.ship_id = ds.ship_id
  INNER JOIN public.dim_ship_type AS dst ON gt.ship_type_id = dst.ship_type_id
WHERE TRUE
  AND cell_x = {{cell_x}}
  AND cell_y = {{cell_y}}
  AND mobile_type = 'Class A'

  {% if from_date and to_date %}
  AND gt.date_id BETWEEN {{from_date}} AND {{to_date}}
  {% endif %}

GROUP BY mmsi,
         ds.name,
         dst.ship_type,
         dst.mobile_type
ORDER BY ds.mmsi;
"""

# noinspection SqlNoDataSourceInspection
draught_query = """
SELECT draught, count(*) as cnt
FROM {{grid_table | sqlsafe}} as gt
  INNER JOIN public.dim_ship AS ds ON gt.ship_id = ds.ship_id
  INNER JOIN public.dim_ship_type AS dst ON gt.ship_type_id = dst.ship_type_id
WHERE TRUE
  AND gt.cell_x = {{cell_x}}
  AND gt.cell_y = {{cell_y}}
  AND dst.mobile_type = 'Class A'
  {% if from_date and to_date %}
  AND gt.date_id BETWEEN {{from_date}} AND {{to_date}}
  {% endif %}
GROUP BY draught
ORDER BY draught DESC NULLS LAST;
"""

# noinspection SqlNoDataSourceInspection
cell_cord_info_query = """
SELECT st_xmin(st_transform(dc.geom, {{srid}})) as lower_left_lon,
       st_ymin(st_transform(dc.geom, {{srid}})) as lower_left_lat,
       st_xmax(st_transform(dc.geom, {{srid}})) as upper_right_lon,
       st_ymax(st_transform(dc.geom, {{srid}})) as upper_right_lat,
       st_x(st_transform(st_centroid(dc.geom), {{srid}})) as center_point_lon,
       st_y(st_transform(st_centroid(dc.geom), {{srid}}))  as center_point_lat 
FROM {{dim_cell | sqlsafe}} as dc
WHERE TRUE
  AND dc.x = {{cell_x}}
  AND dc.y = {{cell_y}};
"""