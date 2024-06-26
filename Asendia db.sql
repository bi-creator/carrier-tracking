-- This script was generated by a beta version of the ERD tool in pgAdmin 4.
-- Please log an issue at https://redmine.postgresql.org/projects/pgadmin4/issues/new if you find any bugs, including reproduction steps.
BEGIN;


CREATE TABLE IF NOT EXISTS public.customers
(
    customer_id integer NOT NULL DEFAULT nextval('customers_customer_id_seq'::regclass),
    customer_name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    customer_email character varying(100) COLLATE pg_catalog."default" NOT NULL,
    customer_phone character varying(20) COLLATE pg_catalog."default" NOT NULL,
    customer_address character varying(255) COLLATE pg_catalog."default" NOT NULL,
    password character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT customers_pkey PRIMARY KEY (customer_id)
);

CREATE TABLE IF NOT EXISTS public.drivers
(
    driver_id integer NOT NULL DEFAULT nextval('drivers_driver_id_seq'::regclass),
    driver_name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    driver_license_number character varying(20) COLLATE pg_catalog."default" NOT NULL,
    driver_phone character varying(20) COLLATE pg_catalog."default" NOT NULL,
    driver_vehicle_plate character varying(20) COLLATE pg_catalog."default" NOT NULL,
    driver_status character varying COLLATE pg_catalog."default",
    CONSTRAINT drivers_pkey PRIMARY KEY (driver_id)
);

CREATE TABLE IF NOT EXISTS public.shipments
(
    shipment_id integer NOT NULL DEFAULT nextval('shipments_shipment_id_seq'::regclass),
    sender_id integer NOT NULL,
    receiver_id integer NOT NULL,
    package_length numeric(10, 2) NOT NULL,
    package_width numeric(10, 2) NOT NULL,
    package_height numeric(10, 2) NOT NULL,
    weight_in_kg numeric(10, 2) NOT NULL,
    package_description text COLLATE pg_catalog."default",
    shipment_status character varying(50) COLLATE pg_catalog."default" DEFAULT 'Pending'::character varying,
    pickup character varying COLLATE pg_catalog."default" NOT NULL,
    drop character varying COLLATE pg_catalog."default" NOT NULL,
    estimated_cost_in_rupes integer NOT NULL,
    estimated_time date NOT NULL,
    CONSTRAINT shipments_pkey PRIMARY KEY (shipment_id)
);

CREATE TABLE IF NOT EXISTS public.shipmenttracking
(
    tracking_id integer NOT NULL DEFAULT nextval('shipmenttracking_tracking_id_seq'::regclass),
    shipment_id integer NOT NULL,
    driver_id integer NOT NULL,
    status_update character varying(255) COLLATE pg_catalog."default" NOT NULL,
    location character varying(100) COLLATE pg_catalog."default" NOT NULL,
    update_time character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT shipmenttracking_pkey PRIMARY KEY (tracking_id)
);

ALTER TABLE IF EXISTS public.shipments
    ADD CONSTRAINT shipments_recipient_id_fkey FOREIGN KEY (receiver_id)
    REFERENCES public.customers (customer_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.shipments
    ADD CONSTRAINT shipments_sender_id_fkey FOREIGN KEY (sender_id)
    REFERENCES public.customers (customer_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.shipmenttracking
    ADD CONSTRAINT shipmenttracking_driver_id_fkey FOREIGN KEY (driver_id)
    REFERENCES public.drivers (driver_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.shipmenttracking
    ADD CONSTRAINT shipmenttracking_shipment_id_fkey FOREIGN KEY (shipment_id)
    REFERENCES public.shipments (shipment_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;

END;