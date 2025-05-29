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
-- Data for Name: admini; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.admini (id, jmeno, prijmeni, email, heslo) FROM stdin;
e1052e4e-dcbf-4402-b8f9-8e9ab287d092	Admin	Admin	admin@firma.com	$2b$12$IFI0GR2rpavllIYZK2vso.Qonc6MyplPFgUvkfu3A9mjIVCmroWuC
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
22a4bfb9d189
\.


--
-- Data for Name: logy_zakazek; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.logy_zakazek (id, zakazka_id, provedl_id, akce, popis, datum) FROM stdin;
\.


--
-- Data for Name: mechanici; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mechanici (id, jmeno, prijmeni, email, heslo, telefon) FROM stdin;
e8b878e8-04d5-4dd4-b729-a0c379c63979	jakub	novy	jakub.novy@firma.com	$2b$12$PvJmZ7.KhkXhrcHh/QxhEOcdqR2FQZOr1o32z0d0YctgAKl7ShXei	123 456 789
e26a3084-3284-4849-a3f0-8dc3196e547c	string	string	user@example.com	$2b$12$wf9Sm3bSFx4muGkj93/85uwajmJHea/5bYnX8GzsAN01/5rgxi5zC	string
a9ec81b0-b425-4d00-9413-b3a5c2242092	petr	novak	petr.novak@firma.com	$2b$12$tk.TA3oD/ybpXhexjNyxnucH4x/5L8f3q6BsKNyD1I2sORd09AX4m	string
9231306f-469e-4f1a-80a4-10893a066279	josef	novak	josef.novak@firma.com	$2b$12$hCj8lYEf1yPuJnp3z9ps2uUw0hx6qTM43fPyQZRU97YoAvQk3HOVy	string
\.


--
-- Data for Name: mechanik_role; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mechanik_role (mechanik_id, role_id) FROM stdin;
e8b878e8-04d5-4dd4-b729-a0c379c63979	e1052e4e-dcbf-4402-b8f9-8e9ab287d092
e26a3084-3284-4849-a3f0-8dc3196e547c	b8592351-7bf0-4e5a-876a-093d3b3b12ec
a9ec81b0-b425-4d00-9413-b3a5c2242092	d714eb04-63da-4e6c-9898-072c9e24392b
a9ec81b0-b425-4d00-9413-b3a5c2242092	b8592351-7bf0-4e5a-876a-093d3b3b12ec
9231306f-469e-4f1a-80a4-10893a066279	b8592351-7bf0-4e5a-876a-093d3b3b12ec
9231306f-469e-4f1a-80a4-10893a066279	d714eb04-63da-4e6c-9898-072c9e24392b
\.


--
-- Data for Name: role; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.role (id, nazev) FROM stdin;
e1052e4e-dcbf-4402-b8f9-8e9ab287d092	vedouci_mechanik
0ac0d6fd-608b-43ae-85cf-01e0adf82c55	specialista_motoru
37337f38-f3af-4301-91c6-88819f606f30	specialista_elektro
a0237b77-22ad-45a8-9308-f1523df74273	specialista_karoserie
b0e36663-01d6-40ee-aad1-748af08a98f2	specialista_zaveseni
d714eb04-63da-4e6c-9898-072c9e24392b	specialista_prevodu
b8592351-7bf0-4e5a-876a-093d3b3b12ec	mlady_mechanik
\.


--
-- Data for Name: zakazky; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.zakazky (id, popis, stav, hotova, datum_prijmu, datum_predani, auto_znacka, auto_model, auto_vin, cena, anonymizovana, smazano, zakaznik_id, mechanik_id, vytvoril_id) FROM stdin;
a557d80a-97b3-4778-951f-a117cb26f209	string	otevřená	f	2025-05-26	2025-05-26	string	string	string	0	f	f	95d46847-2abc-4a6f-a694-20785fb6f222	e8b878e8-04d5-4dd4-b729-a0c379c63979	\N
9322ad3f-2bb1-42ce-8ed8-94ef512f694e	string	otevřená	f	2025-05-26	2025-05-26	string	string	string	0	f	f	95d46847-2abc-4a6f-a694-20785fb6f222	e8b878e8-04d5-4dd4-b729-a0c379c63979	\N
775f8346-7111-4376-8c0c-d8db9b4d1a88	string	string	t	2025-05-26	2025-05-26	string	string	string	0	t	t	95d46847-2abc-4a6f-a694-20785fb6f222	e26a3084-3284-4849-a3f0-8dc3196e547c	\N
46c2bed6-9cc0-45df-b8ad-b2222ccbf779	string	otevřená	f	2025-05-26	2025-05-26	string	string	string	0	f	f	95d46847-2abc-4a6f-a694-20785fb6f222	e8b878e8-04d5-4dd4-b729-a0c379c63979	\N
c2008f61-764a-4052-a8eb-361b3bec3879	string	otevřená	f	2025-05-26	2025-05-26	string	string	string	0	f	f	95d46847-2abc-4a6f-a694-20785fb6f222	e8b878e8-04d5-4dd4-b729-a0c379c63979	\N
80ac2df4-bf34-4409-8800-fff2543312c1	string	otevřená	f	2025-05-26	2025-05-26	string	string	string	0	f	f	95d46847-2abc-4a6f-a694-20785fb6f222	e8b878e8-04d5-4dd4-b729-a0c379c63979	\N
d7e1ec0b-04aa-4369-bd2b-73c81f3b5f88	string	otevřená	f	2025-05-26	2025-05-26	string	string	string	0	f	f	95d46847-2abc-4a6f-a694-20785fb6f222	e8b878e8-04d5-4dd4-b729-a0c379c63979	\N
1e48e77a-e8b9-42b6-921f-9e6067c4bd7f	string	otevřená	f	2025-05-26	2025-05-26	string	string	string	0	f	f	c33e250c-ec13-4577-8111-236b6822a5d6	a9ec81b0-b425-4d00-9413-b3a5c2242092	\N
afe9086e-1c43-4140-9d86-42270bb680eb	string	otevřená	f	2025-05-26	2025-05-26	string	string	string	0	f	f	95d46847-2abc-4a6f-a694-20785fb6f222	e8b878e8-04d5-4dd4-b729-a0c379c63979	\N
4c8adcc9-0949-4bb9-9e77-75daaa2280e2	string	otevřená	f	2025-05-27	2025-05-27	string	string	string	0	f	f	95d46847-2abc-4a6f-a694-20785fb6f222	9231306f-469e-4f1a-80a4-10893a066279	\N
\.


--
-- Data for Name: zakaznici; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.zakaznici (id, jmeno, prijmeni, email, heslo, telefon, adresa, anonymizovan, smazano) FROM stdin;
a0ca1958-c95e-47e3-8d9b-075d47f55d78	Jarda	Vocas	vocas.j@example.com	$2b$12$xB3QwUyXqfnQz/f2FNkDwueKZhyStIlBQkBnVACD/9LiGuca92xnK	666 666 666	v pici	f	f
43c42603-73ea-4efe-b623-c67c02d8829a	Petr	Vocas	vocas.p@example.com	$2b$12$iagpxiPm.VbYeXwJ97BLt.LQcnnKQonx3a3tHSA6lW6NceqdCZCuq	666 666 666	v pici	f	f
c33e250c-ec13-4577-8111-236b6822a5d6	Marie	Debilni	debilni.marie@example.com	$2b$12$rgxtVbHTLB0M2gUAIWD6X.0eOow0VKmCj7IDf1WETYCxqWFuROKEi	112 334 556	Brno-prdel	f	f
1f063e7b-9916-45b1-bc04-70272b73621e	Skolni	Pluk	selekce.debilu@example.com	$2b$12$h9XUjtSWNwUFWdrgSa5HgutpLCJ0a5Ff3rU85LsmhcnaW7diWUdCm	112 334 556	UNOB pico	f	f
95d46847-2abc-4a6f-a694-20785fb6f222	Johnnie	Walker	user@example.com	$2b$12$5TWHmhWYY.rGVYEfgZtI/.1h/H4LPDqQJJ.FH37MdJwUMUYL97bea	string	string	f	f
\.


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
