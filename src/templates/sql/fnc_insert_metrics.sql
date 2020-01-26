-- FUNCTION: public.insert_metrics(json)

-- DROP FUNCTION public.insert_metrics(json);

CREATE OR REPLACE FUNCTION public.insert_metrics(
	metrics_json json)
    RETURNS boolean
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE

AS $BODY$
begin
  insert into metrics_table(record_timestamp, metrics_json) values (now(), metrics_json);
  return True;
end
$BODY$;

ALTER FUNCTION public.insert_metrics(json)
    OWNER TO pguser;

