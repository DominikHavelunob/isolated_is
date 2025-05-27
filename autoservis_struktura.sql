--
-- PostgreSQL database dump
--

-- Dumped from database version 13.21 (Debian 13.21-0+deb11u1)
-- Dumped by pg_dump version 13.21 (Debian 13.21-0+deb11u1)

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: admini; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.admini (
    id uuid NOT NULL,
    jmeno character varying NOT NULL,
    prijmeni character varying NOT NULL,
    email character varying NOT NULL,
    heslo character varying NOT NULL
);


ALTER TABLE public.admini OWNER TO postgres;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: logy_zakazek; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.logy_zakazek (
    id uuid NOT NULL,
    zakazka_id uuid,
    provedl_id uuid,
    akce character varying,
    popis text,
    datum timestamp without time zone
);


ALTER TABLE public.logy_zakazek OWNER TO postgres;

--
-- Name: mechanici; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mechanici (
    id uuid NOT NULL,
    jmeno character varying NOT NULL,
    prijmeni character varying NOT NULL,
    email character varying NOT NULL,
    heslo character varying NOT NULL,
    telefon character varying
);


ALTER TABLE public.mechanici OWNER TO postgres;

--
-- Name: mechanik_role; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mechanik_role (
    mechanik_id uuid,
    role_id uuid
);


ALTER TABLE public.mechanik_role OWNER TO postgres;

--
-- Name: role; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.role (
    id uuid NOT NULL,
    nazev character varying NOT NULL
);


ALTER TABLE public.role OWNER TO postgres;

--
-- Name: zakazky; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.zakazky (
    id uuid NOT NULL,
    popis character varying NOT NULL,
    stav character varying,
    hotova boolean,
    datum_prijmu date,
    datum_predani date,
    auto_znacka character varying,
    auto_model character varying,
    auto_vin character varying,
    cena double precision,
    anonymizovana boolean,
    smazano boolean,
    zakaznik_id uuid,
    mechanik_id uuid,
    vytvoril_id uuid
);


ALTER TABLE public.zakazky OWNER TO postgres;

--
-- Name: zakaznici; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.zakaznici (
    id uuid NOT NULL,
    jmeno character varying NOT NULL,
    prijmeni character varying NOT NULL,
    email character varying NOT NULL,
    heslo character varying NOT NULL,
    telefon character varying,
    adresa character varying,
    anonymizovan boolean,
    smazano boolean
);


ALTER TABLE public.zakaznici OWNER TO postgres;

--
-- Name: admini admini_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admini
    ADD CONSTRAINT admini_pkey PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: logy_zakazek logy_zakazek_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logy_zakazek
    ADD CONSTRAINT logy_zakazek_pkey PRIMARY KEY (id);


--
-- Name: mechanici mechanici_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mechanici
    ADD CONSTRAINT mechanici_email_key UNIQUE (email);


--
-- Name: mechanici mechanici_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mechanici
    ADD CONSTRAINT mechanici_pkey PRIMARY KEY (id);


--
-- Name: role role_nazev_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role
    ADD CONSTRAINT role_nazev_key UNIQUE (nazev);


--
-- Name: role role_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role
    ADD CONSTRAINT role_pkey PRIMARY KEY (id);


--
-- Name: zakazky zakazky_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.zakazky
    ADD CONSTRAINT zakazky_pkey PRIMARY KEY (id);


--
-- Name: zakaznici zakaznici_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.zakaznici
    ADD CONSTRAINT zakaznici_email_key UNIQUE (email);


--
-- Name: zakaznici zakaznici_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.zakaznici
    ADD CONSTRAINT zakaznici_pkey PRIMARY KEY (id);


--
-- Name: ix_admini_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_admini_email ON public.admini USING btree (email);


--
-- Name: logy_zakazek logy_zakazek_zakazka_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logy_zakazek
    ADD CONSTRAINT logy_zakazek_zakazka_id_fkey FOREIGN KEY (zakazka_id) REFERENCES public.zakazky(id);


--
-- Name: mechanik_role mechanik_role_mechanik_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mechanik_role
    ADD CONSTRAINT mechanik_role_mechanik_id_fkey FOREIGN KEY (mechanik_id) REFERENCES public.mechanici(id);


--
-- Name: mechanik_role mechanik_role_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mechanik_role
    ADD CONSTRAINT mechanik_role_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.role(id);


--
-- Name: zakazky zakazky_mechanik_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.zakazky
    ADD CONSTRAINT zakazky_mechanik_id_fkey FOREIGN KEY (mechanik_id) REFERENCES public.mechanici(id);


--
-- Name: zakazky zakazky_vytvoril_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.zakazky
    ADD CONSTRAINT zakazky_vytvoril_id_fkey FOREIGN KEY (vytvoril_id) REFERENCES public.admini(id);


--
-- Name: zakazky zakazky_zakaznik_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.zakazky
    ADD CONSTRAINT zakazky_zakaznik_id_fkey FOREIGN KEY (zakaznik_id) REFERENCES public.zakaznici(id);


--
-- PostgreSQL database dump complete
--

