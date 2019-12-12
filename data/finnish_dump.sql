--
-- PostgreSQL database dump
--

-- Dumped from database version 11.5 (Ubuntu 11.5-1build1)
-- Dumped by pg_dump version 11.5 (Ubuntu 11.5-1build1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE ONLY public.finnish DROP CONSTRAINT finnish_pkey;
ALTER TABLE public.finnish ALTER COLUMN id DROP DEFAULT;
DROP SEQUENCE public.finnish_id_seq;
DROP TABLE public.finnish;
SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: finnish; Type: TABLE; Schema: public; Owner: fabio
--

CREATE TABLE public.finnish (
    id integer NOT NULL,
    word character varying(100),
    meaning character varying(2555),
    test character varying(2555)
);


ALTER TABLE public.finnish OWNER TO fabio;

--
-- Name: finnish_id_seq; Type: SEQUENCE; Schema: public; Owner: fabio
--

CREATE SEQUENCE public.finnish_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.finnish_id_seq OWNER TO fabio;

--
-- Name: finnish_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: fabio
--

ALTER SEQUENCE public.finnish_id_seq OWNED BY public.finnish.id;


--
-- Name: finnish id; Type: DEFAULT; Schema: public; Owner: fabio
--

ALTER TABLE ONLY public.finnish ALTER COLUMN id SET DEFAULT nextval('public.finnish_id_seq'::regclass);


--
-- Data for Name: finnish; Type: TABLE DATA; Schema: public; Owner: fabio
--

INSERT INTO public.finnish VALUES (1, 'talo', 'house, building', NULL);
INSERT INTO public.finnish VALUES (2, 'kiitos', 'thank you', NULL);
INSERT INTO public.finnish VALUES (3, 'terve', 'healthy, sane', NULL);
INSERT INTO public.finnish VALUES (4, 'ääntäminen', 'pronounciation', NULL);
INSERT INTO public.finnish VALUES (5, 'tervetuloa', 'welcome', NULL);
INSERT INTO public.finnish VALUES (6, 'anteeksi', '(I’m) sorry, excuse me?, (I beg your) pardon', NULL);
INSERT INTO public.finnish VALUES (7, 'onko', 'is (there)?', NULL);
INSERT INTO public.finnish VALUES (8, 'suomen kurssi', 'Finnish (language) course', NULL);
INSERT INTO public.finnish VALUES (9, 'minä', 'I', NULL);
INSERT INTO public.finnish VALUES (10, 'samoin', 'same to you, the same, likewise', NULL);


--
-- Name: finnish_id_seq; Type: SEQUENCE SET; Schema: public; Owner: fabio
--

SELECT pg_catalog.setval('public.finnish_id_seq', 10, true);


--
-- Name: finnish finnish_pkey; Type: CONSTRAINT; Schema: public; Owner: fabio
--

ALTER TABLE ONLY public.finnish
    ADD CONSTRAINT finnish_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

