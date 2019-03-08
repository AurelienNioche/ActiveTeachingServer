--
-- PostgreSQL database dump
--

-- Dumped from database version 11.2
-- Dumped by pg_dump version 11.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: question; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.question VALUES (50, 6, 0, '虫', 'Insect', 'Power', 'Two', 'Insect', 'Leg', 'Flower', 'Eight', 'Flower', '2019-03-08 10:12:54.503194+02', '2019-03-08 10:12:58.653191+02');
INSERT INTO public.question VALUES (51, 6, 1, '八', 'Eight', 'Two', 'Flower', 'King', 'Insect', 'Eight', 'Inside', 'Flower', '2019-03-08 10:13:01.584535+02', '2019-03-08 10:13:09.10222+02');
INSERT INTO public.question VALUES (52, 6, 2, '中', 'Inside', 'Inside', 'Living', 'Two', 'Insect', 'Flower', 'Power', 'Inside', '2019-03-08 10:13:10.718823+02', '2019-03-08 10:13:15.735366+02');
INSERT INTO public.question VALUES (53, 6, 3, '生', 'Living', 'Leg', 'Eight', 'Living', 'Seven', 'Flower', 'Two', 'Two', '2019-03-08 10:13:16.768492+02', '2019-03-08 10:13:22.867624+02');
INSERT INTO public.question VALUES (54, 6, 4, '生', 'Living', 'Living', 'Flower', 'Power', 'Insect', 'Two', 'Eight', 'Living', '2019-03-08 10:13:25.200335+02', '2019-03-08 10:13:30.685515+02');
INSERT INTO public.question VALUES (55, 6, 5, '八', 'Eight', 'Two', 'Living', 'Flower', 'Leg', 'Insect', 'Eight', 'Eight', '2019-03-08 10:13:31.7353+02', '2019-03-08 10:13:34.202196+02');
INSERT INTO public.question VALUES (56, 6, 6, '虫', 'Insect', 'Inside', 'Flower', 'Power', 'Living', 'Seven', 'Insect', 'Flower', '2019-03-08 10:13:35.252077+02', '2019-03-08 10:13:38.95173+02');
INSERT INTO public.question VALUES (57, 6, 7, '八', 'Eight', 'Leg', 'Eight', 'Two', 'Flower', 'Living', 'Insect', 'Eight', '2019-03-08 10:13:40.185423+02', '2019-03-08 10:13:41.952178+02');
INSERT INTO public.question VALUES (58, 6, 8, '虫', 'Insect', 'King', 'Power', 'Flower', 'Insect', 'Leg', 'Seven', 'Insect', '2019-03-08 10:13:43.002119+02', '2019-03-08 10:13:48.952142+02');
INSERT INTO public.question VALUES (59, 6, 9, '力', 'Power', 'Leg', 'Eight', 'Flower', 'Power', 'Inside', 'Living', 'Power', '2019-03-08 10:13:50.001357+02', '2019-03-08 10:13:55.101865+02');
INSERT INTO public.question VALUES (60, 6, 10, '中', 'Inside', 'Leg', 'Inside', 'Power', 'Eight', 'Seven', 'Insect', 'Inside', '2019-03-08 10:13:56.152134+02', '2019-03-08 10:14:01.752227+02');
INSERT INTO public.question VALUES (61, 6, 11, '八', 'Eight', 'Eight', 'Power', 'King', 'Inside', 'Insect', 'Leg', 'Eight', '2019-03-08 10:14:02.802074+02', '2019-03-08 10:14:04.602132+02');
INSERT INTO public.question VALUES (62, 6, 12, '生', 'Living', 'Inside', 'Insect', 'Living', 'King', 'Leg', 'Seven', 'Inside', '2019-03-08 10:14:05.652328+02', '2019-03-08 10:14:10.235477+02');
INSERT INTO public.question VALUES (63, 6, 13, '虫', 'Insect', 'Power', 'King', 'Living', 'Two', 'Flower', 'Insect', 'Insect', '2019-03-08 10:14:12.451815+02', '2019-03-08 10:14:15.81853+02');
INSERT INTO public.question VALUES (64, 6, 14, '王', 'King', 'Living', 'King', 'Leg', 'Eight', 'Seven', 'Inside', 'King', '2019-03-08 10:14:16.868827+02', '2019-03-08 10:14:22.4188+02');
INSERT INTO public.question VALUES (65, 6, 15, '花', 'Flower', 'Flower', 'Seven', 'Leg', 'Two', 'Eight', 'Power', 'Power', '2019-03-08 10:14:23.468873+02', '2019-03-08 10:14:28.852058+02');
INSERT INTO public.question VALUES (66, 6, 16, '力', 'Power', 'Eight', 'Inside', 'Power', 'Flower', 'Seven', 'Leg', 'Power', '2019-03-08 10:14:30.835073+02', '2019-03-08 10:14:37.285402+02');
INSERT INTO public.question VALUES (67, 6, 17, '王', 'King', 'Eight', 'Inside', 'King', 'Insect', 'Seven', 'Living', 'Eight', '2019-03-08 10:14:38.335478+02', '2019-03-08 10:14:45.985313+02');
INSERT INTO public.question VALUES (68, 6, 18, '虫', 'Insect', 'King', 'Inside', 'Insect', 'Leg', 'Eight', 'Living', 'Inside', '2019-03-08 10:14:48.03502+02', '2019-03-08 10:14:54.935529+02');
INSERT INTO public.question VALUES (69, 6, 19, '王', 'King', 'Living', 'Seven', 'King', 'Insect', 'Power', 'Leg', 'King', '2019-03-08 10:14:56.268833+02', '2019-03-08 10:15:09.000897+02');
INSERT INTO public.question VALUES (70, 6, 20, '足', 'Leg', 'Seven', 'Two', 'Living', 'Flower', 'Power', 'Leg', 'Living', '2019-03-08 10:15:10.050786+02', '2019-03-08 10:15:12.201292+02');
INSERT INTO public.question VALUES (71, 6, 21, '足', 'Leg', 'Insect', 'Two', 'Leg', 'Seven', 'Flower', 'Living', 'Leg', '2019-03-08 10:15:13.317131+02', '2019-03-08 10:15:16.517357+02');
INSERT INTO public.question VALUES (72, 6, 22, '二', 'Two', 'Inside', 'Two', 'Flower', 'Insect', 'King', 'Eight', 'Two', '2019-03-08 10:15:17.551273+02', '2019-03-08 10:15:20.817929+02');
INSERT INTO public.question VALUES (73, 6, 23, '七', 'Seven', 'Insect', 'King', 'Flower', 'Seven', 'Eight', 'Living', 'Seven', '2019-03-08 10:15:21.86796+02', '2019-03-08 10:15:34.918881+02');
INSERT INTO public.question VALUES (74, 6, 24, '二', 'Two', 'King', 'Inside', 'Two', 'Living', 'Power', 'Insect', 'Two', '2019-03-08 10:15:35.968117+02', '2019-03-08 10:15:38.068411+02');
INSERT INTO public.question VALUES (75, 6, 25, '二', 'Two', 'Seven', 'Insect', 'Eight', 'Flower', 'Two', 'Power', 'Two', '2019-03-08 10:15:39.117838+02', '2019-03-08 10:15:41.484282+02');
INSERT INTO public.question VALUES (76, 6, 26, '花', 'Flower', 'King', 'Inside', 'Power', 'Insect', 'Living', 'Flower', 'Flower', '2019-03-08 10:15:42.534953+02', '2019-03-08 10:15:46.502268+02');
INSERT INTO public.question VALUES (77, 6, 27, '虫', 'Insect', 'Seven', 'Living', 'Eight', 'King', 'Inside', 'Insect', 'Living', '2019-03-08 10:15:47.551606+02', '2019-03-08 10:15:54.98455+02');
INSERT INTO public.question VALUES (78, 6, 28, '力', 'Power', 'Power', 'Inside', 'King', 'Two', 'Living', 'Flower', 'Power', '2019-03-08 10:15:56.752+02', '2019-03-08 10:16:02.918581+02');
INSERT INTO public.question VALUES (79, 6, 29, '王', 'King', 'King', 'Insect', 'Eight', 'Two', 'Power', 'Living', 'Eight', '2019-03-08 10:16:03.967944+02', '2019-03-08 10:16:05.418027+02');
INSERT INTO public.question VALUES (80, 6, 30, '花', 'Flower', 'Insect', 'Flower', 'Power', 'Leg', 'Eight', 'Seven', 'Leg', '2019-03-08 10:16:07.217977+02', '2019-03-08 10:16:17.084792+02');
INSERT INTO public.question VALUES (81, 6, 31, '二', 'Two', 'Eight', 'King', 'Inside', 'Flower', 'Seven', 'Two', 'Two', '2019-03-08 10:16:18.435017+02', '2019-03-08 10:16:19.93423+02');
INSERT INTO public.question VALUES (82, 6, 32, '足', 'Leg', 'Eight', 'Flower', 'Leg', 'Power', 'Living', 'Seven', 'Flower', '2019-03-08 10:16:20.968891+02', '2019-03-08 10:16:25.001003+02');
INSERT INTO public.question VALUES (83, 6, 33, '虫', 'Insect', 'Insect', 'Living', 'Seven', 'King', 'Eight', 'Two', 'Living', '2019-03-08 10:16:26.251953+02', '2019-03-08 10:16:33.634744+02');
INSERT INTO public.question VALUES (84, 6, 34, '花', 'Flower', 'Flower', 'Inside', 'Power', 'Two', 'Eight', 'King', 'Inside', '2019-03-08 10:16:34.568249+02', '2019-03-08 10:16:40.751458+02');
INSERT INTO public.question VALUES (85, 6, 35, '八', 'Eight', 'Eight', 'Insect', 'Leg', 'Power', 'Inside', 'King', 'Eight', '2019-03-08 10:16:41.818691+02', '2019-03-08 10:16:43.885322+02');
INSERT INTO public.question VALUES (86, 6, 36, '虫', 'Insect', 'Eight', 'Inside', 'Seven', 'Insect', 'Leg', 'Two', 'Leg', '2019-03-08 10:16:44.934575+02', '2019-03-08 10:16:52.450991+02');
INSERT INTO public.question VALUES (87, 6, 37, '虫', 'Insect', 'Inside', 'King', 'Insect', 'Living', 'Eight', 'Flower', 'Living', '2019-03-08 10:16:53.418152+02', '2019-03-08 10:16:57.15114+02');
INSERT INTO public.question VALUES (88, 6, 38, '力', 'Power', 'Power', 'Flower', 'Two', 'Eight', 'Insect', 'Seven', 'Power', '2019-03-08 10:16:58.734909+02', '2019-03-08 10:17:04.984482+02');
INSERT INTO public.question VALUES (89, 6, 39, '足', 'Leg', 'Eight', 'Power', 'Flower', 'Two', 'Seven', 'Leg', 'Leg', '2019-03-08 10:17:06.034488+02', '2019-03-08 10:17:16.067651+02');
INSERT INTO public.question VALUES (90, 6, 40, '力', 'Power', 'Living', 'Power', 'Inside', 'Flower', 'Eight', 'Insect', 'Power', '2019-03-08 10:17:17.117513+02', '2019-03-08 10:17:20.767354+02');
INSERT INTO public.question VALUES (91, 6, 41, '力', 'Power', 'King', 'Power', 'Seven', 'Two', 'Eight', 'Flower', 'Power', '2019-03-08 10:17:21.817761+02', '2019-03-08 10:17:23.333433+02');
INSERT INTO public.question VALUES (92, 6, 42, '花', 'Flower', 'Two', 'Seven', 'Eight', 'Leg', 'Flower', 'Power', 'Flower', '2019-03-08 10:17:24.384445+02', '2019-03-08 10:17:31.367656+02');
INSERT INTO public.question VALUES (93, 6, 43, '八', 'Eight', 'Power', 'Leg', 'Insect', 'Inside', 'Eight', 'Flower', 'Eight', '2019-03-08 10:17:32.417399+02', '2019-03-08 10:17:34.285398+02');
INSERT INTO public.question VALUES (94, 6, 44, '二', 'Two', 'Eight', 'Two', 'Seven', 'Power', 'Leg', 'Living', 'Two', '2019-03-08 10:17:35.334467+02', '2019-03-08 10:17:36.768831+02');
INSERT INTO public.question VALUES (95, 6, 45, '八', 'Eight', 'Eight', 'Insect', 'Seven', 'King', 'Power', 'Flower', 'Eight', '2019-03-08 10:17:37.818556+02', '2019-03-08 10:17:40.035456+02');
INSERT INTO public.question VALUES (96, 6, 46, '八', 'Eight', 'Eight', 'Insect', 'Leg', 'Power', 'King', 'Inside', 'Eight', '2019-03-08 10:17:41.067247+02', '2019-03-08 10:17:42.585291+02');
INSERT INTO public.question VALUES (97, 6, 47, '七', 'Seven', 'King', 'Seven', 'Living', 'Flower', 'Leg', 'Inside', 'Seven', '2019-03-08 10:17:43.635128+02', '2019-03-08 10:17:48.502254+02');
INSERT INTO public.question VALUES (98, 6, 48, '虫', 'Insect', 'Seven', 'Power', 'Insect', 'Living', 'Inside', 'King', 'Insect', '2019-03-08 10:17:49.55118+02', '2019-03-08 10:17:56.184328+02');
INSERT INTO public.question VALUES (99, 6, 49, '生', 'Living', 'Two', 'Living', 'Inside', 'Flower', 'Insect', 'Seven', 'Living', '2019-03-08 10:17:57.235192+02', '2019-03-08 10:18:12.684808+02');
INSERT INTO public.question VALUES (100, 6, 50, '力', 'Power', 'Power', 'Insect', 'Living', 'King', 'Two', 'Leg', 'Power', '2019-03-08 10:18:13.734221+02', '2019-03-08 10:18:17.835397+02');
INSERT INTO public.question VALUES (101, 6, 51, '虫', 'Insect', 'King', 'Leg', 'Insect', 'Flower', 'Living', 'Inside', 'Leg', '2019-03-08 10:18:18.868326+02', '2019-03-08 10:18:21.901961+02');
INSERT INTO public.question VALUES (102, 6, 52, '足', 'Leg', 'Two', 'Eight', 'Power', 'Leg', 'Flower', 'Inside', 'Leg', '2019-03-08 10:18:23.20165+02', '2019-03-08 10:18:26.152113+02');
INSERT INTO public.question VALUES (103, 6, 53, '八', 'Eight', 'Seven', 'Inside', 'King', 'Flower', 'Leg', 'Eight', 'Eight', '2019-03-08 10:18:27.202074+02', '2019-03-08 10:18:29.018774+02');
INSERT INTO public.question VALUES (104, 6, 54, '虫', 'Insect', 'Flower', 'King', 'Leg', 'Insect', 'Inside', 'Two', 'Insect', '2019-03-08 10:18:30.06824+02', '2019-03-08 10:18:37.885487+02');
INSERT INTO public.question VALUES (105, 6, 55, '虫', 'Insect', 'Seven', 'Eight', 'Two', 'Flower', 'Insect', 'Living', 'Insect', '2019-03-08 10:18:38.935462+02', '2019-03-08 10:18:41.11875+02');
INSERT INTO public.question VALUES (106, 6, 56, '足', 'Leg', 'Living', 'Flower', 'Insect', 'Leg', 'Seven', 'Two', 'Leg', '2019-03-08 10:18:42.167364+02', '2019-03-08 10:18:44.934205+02');
INSERT INTO public.question VALUES (107, 6, 57, '力', 'Power', 'Power', 'Flower', 'King', 'Eight', 'Leg', 'Inside', 'Power', '2019-03-08 10:18:45.968392+02', '2019-03-08 10:18:49.96854+02');
INSERT INTO public.question VALUES (108, 6, 58, '八', 'Eight', 'Leg', 'Insect', 'Eight', 'Power', 'Flower', 'Seven', 'Eight', '2019-03-08 10:18:51.017888+02', '2019-03-08 10:18:53.467509+02');
INSERT INTO public.question VALUES (109, 6, 59, '虫', 'Insect', 'King', 'Power', 'Seven', 'Inside', 'Insect', 'Flower', 'Flower', '2019-03-08 10:18:54.518687+02', '2019-03-08 10:19:01.751644+02');
INSERT INTO public.question VALUES (110, 6, 60, '七', 'Seven', 'Inside', 'Seven', 'Insect', 'Leg', 'Eight', 'Flower', 'Seven', '2019-03-08 10:19:03.085249+02', '2019-03-08 10:19:05.250714+02');
INSERT INTO public.question VALUES (111, 6, 61, '花', 'Flower', 'Living', 'Seven', 'Flower', 'Two', 'Leg', 'King', 'Flower', '2019-03-08 10:19:06.301129+02', '2019-03-08 10:19:12.935333+02');
INSERT INTO public.question VALUES (112, 6, 62, '虫', 'Insect', 'Leg', 'Insect', 'Inside', 'Power', 'King', 'Two', 'Leg', '2019-03-08 10:19:13.967864+02', '2019-03-08 10:19:16.302189+02');
INSERT INTO public.question VALUES (113, 6, 63, '生', 'Living', 'Leg', 'Flower', 'Living', 'Two', 'King', 'Power', 'Flower', '2019-03-08 10:19:17.568829+02', '2019-03-08 10:19:23.551966+02');
INSERT INTO public.question VALUES (114, 6, 64, '虫', 'Insect', 'Leg', 'Seven', 'Eight', 'Insect', 'Inside', 'King', 'Leg', '2019-03-08 10:19:24.601979+02', '2019-03-08 10:19:26.601515+02');
INSERT INTO public.question VALUES (115, 6, 65, '力', 'Power', 'Two', 'King', 'Power', 'Inside', 'Leg', 'Living', 'Power', '2019-03-08 10:19:27.768937+02', '2019-03-08 10:19:33.652248+02');
INSERT INTO public.question VALUES (116, 6, 66, '二', 'Two', 'Eight', 'Seven', 'Inside', 'Leg', 'Two', 'Insect', 'Two', '2019-03-08 10:19:34.70216+02', '2019-03-08 10:19:36.184232+02');
INSERT INTO public.question VALUES (117, 6, 67, '二', 'Two', 'Flower', 'Living', 'Two', 'King', 'Inside', 'Power', 'Two', '2019-03-08 10:19:37.234363+02', '2019-03-08 10:19:39.935067+02');
INSERT INTO public.question VALUES (118, 6, 68, '花', 'Flower', 'Seven', 'Leg', 'Inside', 'King', 'Eight', 'Flower', 'Leg', '2019-03-08 10:19:40.968454+02', '2019-03-08 10:19:46.551312+02');
INSERT INTO public.question VALUES (119, 6, 69, '生', 'Living', 'Living', 'King', 'Inside', 'Leg', 'Two', 'Flower', 'Living', '2019-03-08 10:19:47.735612+02', '2019-03-08 10:19:55.102072+02');
INSERT INTO public.question VALUES (120, 6, 70, '虫', 'Insect', 'Flower', 'Two', 'King', 'Insect', 'Seven', 'Leg', 'Leg', '2019-03-08 10:19:56.15181+02', '2019-03-08 10:19:58.7678+02');
INSERT INTO public.question VALUES (121, 6, 71, '二', 'Two', 'Flower', 'Two', 'Living', 'Power', 'King', 'Leg', 'Two', '2019-03-08 10:20:00.38553+02', '2019-03-08 10:20:03.201238+02');
INSERT INTO public.question VALUES (122, 6, 72, '力', 'Power', 'Power', 'Flower', 'Eight', 'Leg', 'Seven', 'King', 'Power', '2019-03-08 10:20:04.233571+02', '2019-03-08 10:20:06.168851+02');
INSERT INTO public.question VALUES (123, 6, 73, '虫', 'Insect', 'Power', 'King', 'Insect', 'Flower', 'Leg', 'Two', 'Insect', '2019-03-08 10:20:07.217836+02', '2019-03-08 10:20:11.435134+02');
INSERT INTO public.question VALUES (124, 6, 74, '二', 'Two', 'King', 'Inside', 'Power', 'Flower', 'Two', 'Living', 'Two', '2019-03-08 10:20:12.45047+02', '2019-03-08 10:20:14.084688+02');
INSERT INTO public.question VALUES (125, 6, 75, '二', 'Two', 'Seven', 'Flower', 'Leg', 'Two', 'Insect', 'Living', 'Two', '2019-03-08 10:20:15.135438+02', '2019-03-08 10:20:17.568846+02');
INSERT INTO public.question VALUES (126, 6, 76, '八', 'Eight', 'Insect', 'Living', 'Inside', 'Seven', 'Two', 'Eight', 'Eight', '2019-03-08 10:20:18.617819+02', '2019-03-08 10:20:21.352153+02');
INSERT INTO public.question VALUES (127, 6, 77, '八', 'Eight', 'King', 'Leg', 'Power', 'Seven', 'Flower', 'Eight', 'Eight', '2019-03-08 10:20:22.402196+02', '2019-03-08 10:20:23.635307+02');
INSERT INTO public.question VALUES (128, 6, 78, '八', 'Eight', 'Two', 'Power', 'Flower', 'Insect', 'Eight', 'King', 'Eight', '2019-03-08 10:20:24.668581+02', '2019-03-08 10:20:27.13553+02');
INSERT INTO public.question VALUES (129, 6, 79, '虫', 'Insect', 'Inside', 'Living', 'Two', 'Leg', 'Seven', 'Insect', 'Insect', '2019-03-08 10:20:28.168203+02', '2019-03-08 10:20:33.485483+02');
INSERT INTO public.question VALUES (130, 6, 80, '王', 'King', 'Flower', 'Seven', 'Inside', 'Eight', 'Insect', 'King', 'Eight', '2019-03-08 10:20:34.534367+02', '2019-03-08 10:20:36.684999+02');
INSERT INTO public.question VALUES (131, 6, 81, '力', 'Power', 'Flower', 'Two', 'Inside', 'Seven', 'Power', 'Leg', 'Power', '2019-03-08 10:20:38.300883+02', '2019-03-08 10:20:40.735728+02');
INSERT INTO public.question VALUES (132, 6, 82, '力', 'Power', 'King', 'Eight', 'Two', 'Inside', 'Seven', 'Power', 'Power', '2019-03-08 10:20:41.767911+02', '2019-03-08 10:20:44.302229+02');
INSERT INTO public.question VALUES (133, 6, 83, '力', 'Power', 'Insect', 'Living', 'King', 'Power', 'Two', 'Seven', 'Power', '2019-03-08 10:20:45.352248+02', '2019-03-08 10:20:47.034356+02');
INSERT INTO public.question VALUES (134, 6, 84, '生', 'Living', 'Eight', 'Two', 'Leg', 'Living', 'Power', 'Flower', 'Living', '2019-03-08 10:20:48.068571+02', '2019-03-08 10:20:59.369055+02');
INSERT INTO public.question VALUES (135, 6, 85, '王', 'King', 'King', 'Insect', 'Two', 'Leg', 'Seven', 'Inside', 'King', '2019-03-08 10:21:00.418914+02', '2019-03-08 10:21:04.45206+02');
INSERT INTO public.question VALUES (136, 6, 86, '虫', 'Insect', 'Insect', 'Flower', 'Inside', 'Power', 'Eight', 'Two', 'Insect', '2019-03-08 10:21:05.501332+02', '2019-03-08 10:21:21.952025+02');
INSERT INTO public.question VALUES (137, 6, 87, '八', 'Eight', 'Two', 'Living', 'Eight', 'Seven', 'Flower', 'Inside', 'Eight', '2019-03-08 10:21:23.001851+02', '2019-03-08 10:21:24.852181+02');
INSERT INTO public.question VALUES (138, 6, 88, '八', 'Eight', 'Two', 'Eight', 'Leg', 'Flower', 'King', 'Insect', 'Eight', '2019-03-08 10:21:25.90221+02', '2019-03-08 10:21:27.752218+02');
INSERT INTO public.question VALUES (139, 6, 89, '王', 'King', 'Insect', 'Power', 'Eight', 'King', 'Seven', 'Leg', 'Eight', '2019-03-08 10:21:28.802186+02', '2019-03-08 10:21:35.135593+02');
INSERT INTO public.question VALUES (140, 6, 90, '虫', 'Insect', 'Living', 'Power', 'Leg', 'Eight', 'Insect', 'Flower', 'Living', '2019-03-08 10:21:36.735581+02', '2019-03-08 10:21:43.352267+02');
INSERT INTO public.question VALUES (141, 6, 91, '二', 'Two', 'Flower', 'Power', 'Eight', 'Two', 'Living', 'Seven', 'Two', '2019-03-08 10:21:44.485588+02', '2019-03-08 10:21:47.785585+02');
INSERT INTO public.question VALUES (142, 6, 92, '七', 'Seven', 'Two', 'Insect', 'Leg', 'King', 'Seven', 'Flower', 'Seven', '2019-03-08 10:21:48.835342+02', '2019-03-08 10:21:51.552249+02');
INSERT INTO public.question VALUES (143, 6, 93, '虫', 'Insect', 'Inside', 'Flower', 'Eight', 'King', 'Two', 'Insect', 'Insect', '2019-03-08 10:21:52.601352+02', '2019-03-08 10:21:57.802237+02');
INSERT INTO public.question VALUES (144, 6, 94, '花', 'Flower', 'Insect', 'Living', 'Flower', 'Seven', 'King', 'Power', 'Living', '2019-03-08 10:21:58.852179+02', '2019-03-08 10:22:04.568998+02');
INSERT INTO public.question VALUES (145, 6, 95, '七', 'Seven', 'Inside', 'Leg', 'Insect', 'Seven', 'Two', 'Power', 'Seven', '2019-03-08 10:22:05.585244+02', '2019-03-08 10:22:07.201698+02');
INSERT INTO public.question VALUES (146, 6, 96, '八', 'Eight', 'King', 'Eight', 'Insect', 'Flower', 'Leg', 'Seven', 'Eight', '2019-03-08 10:22:08.252168+02', '2019-03-08 10:22:10.218965+02');
INSERT INTO public.question VALUES (147, 6, 97, '虫', 'Insect', 'Power', 'Insect', 'King', 'Leg', 'Flower', 'Living', 'Living', '2019-03-08 10:22:11.268037+02', '2019-03-08 10:22:18.13552+02');
INSERT INTO public.question VALUES (148, 6, 98, '二', 'Two', 'Seven', 'King', 'Eight', 'Two', 'Leg', 'Insect', 'Two', '2019-03-08 10:22:21.034718+02', '2019-03-08 10:22:22.768564+02');
INSERT INTO public.question VALUES (149, 6, 99, '中', 'Inside', 'King', 'Insect', 'Inside', 'Leg', 'Living', 'Flower', 'Leg', '2019-03-08 10:22:23.818472+02', '2019-03-08 10:22:28.518348+02');
INSERT INTO public.question VALUES (150, 7, 0, '虫', 'Insect', 'Power', 'Two', 'Insect', 'Leg', 'Flower', 'Eight', 'Flower', '2019-03-08 10:45:34.407634+02', '2019-03-08 10:45:48.80705+02');
INSERT INTO public.question VALUES (151, 7, 1, '八', 'Eight', 'Two', 'Flower', 'King', 'Insect', 'Eight', 'Inside', 'King', '2019-03-08 10:45:54.272344+02', '2019-03-08 10:46:02.539612+02');
INSERT INTO public.question VALUES (152, 7, 2, '中', 'Inside', 'Inside', 'Living', 'Two', 'Insect', 'Flower', 'Power', 'Flower', '2019-03-08 10:46:05.555384+02', '2019-03-08 10:46:10.439582+02');
INSERT INTO public.question VALUES (153, 7, 3, '生', 'Living', 'Leg', 'Eight', 'Living', 'Seven', 'Flower', 'Two', 'Living', '2019-03-08 10:46:14.35577+02', '2019-03-08 10:46:18.756232+02');
INSERT INTO public.question VALUES (154, 7, 4, '生', 'Living', 'Living', 'Flower', 'Power', 'Insect', 'Two', 'Eight', 'Living', '2019-03-08 10:46:19.806181+02', '2019-03-08 10:46:24.323291+02');
INSERT INTO public.question VALUES (155, 7, 5, '八', 'Eight', 'Two', 'Living', 'Flower', 'Leg', 'Insect', 'Eight', 'Eight', '2019-03-08 10:46:25.372394+02', '2019-03-08 10:46:30.690158+02');
INSERT INTO public.question VALUES (156, 7, 6, '虫', 'Insect', 'Inside', 'Flower', 'Power', 'Living', 'Seven', 'Insect', 'Insect', '2019-03-08 10:46:31.739791+02', '2019-03-08 10:46:37.740451+02');
INSERT INTO public.question VALUES (157, 7, 7, '八', 'Eight', 'Leg', 'Eight', 'Two', 'Flower', 'Living', 'Insect', 'Eight', '2019-03-08 10:46:38.790079+02', '2019-03-08 10:46:41.506808+02');
INSERT INTO public.question VALUES (158, 7, 8, '虫', 'Insect', 'King', 'Power', 'Flower', 'Insect', 'Leg', 'Seven', 'Insect', '2019-03-08 10:46:42.539428+02', '2019-03-08 10:46:45.622812+02');
INSERT INTO public.question VALUES (159, 7, 9, '力', 'Power', 'Leg', 'Eight', 'Flower', 'Power', 'Inside', 'Living', 'Leg', '2019-03-08 10:46:46.67257+02', '2019-03-08 10:46:55.840099+02');
INSERT INTO public.question VALUES (160, 7, 10, '中', 'Inside', 'Leg', 'Inside', 'Power', 'Eight', 'Seven', 'Insect', 'Inside', '2019-03-08 10:46:58.489811+02', '2019-03-08 10:47:02.640346+02');
INSERT INTO public.question VALUES (161, 7, 11, '八', 'Eight', 'Eight', 'Power', 'King', 'Inside', 'Insect', 'Leg', 'Eight', '2019-03-08 10:47:03.689773+02', '2019-03-08 10:47:06.423681+02');
INSERT INTO public.question VALUES (162, 7, 12, '生', 'Living', 'Inside', 'Insect', 'Living', 'King', 'Leg', 'Seven', 'Living', '2019-03-08 10:47:07.473599+02', '2019-03-08 10:47:10.140803+02');
INSERT INTO public.question VALUES (163, 7, 13, '虫', 'Insect', 'Power', 'King', 'Living', 'Two', 'Flower', 'Insect', 'Insect', '2019-03-08 10:47:11.19041+02', '2019-03-08 10:47:13.356555+02');
INSERT INTO public.question VALUES (164, 7, 14, '王', 'King', 'Living', 'King', 'Leg', 'Eight', 'Seven', 'Inside', 'Seven', '2019-03-08 10:47:14.406115+02', '2019-03-08 10:47:19.339768+02');
INSERT INTO public.question VALUES (165, 7, 15, '花', 'Flower', 'Flower', 'Seven', 'Leg', 'Two', 'Eight', 'Power', 'Flower', '2019-03-08 10:47:21.539453+02', '2019-03-08 10:47:31.122431+02');
INSERT INTO public.question VALUES (166, 7, 16, '力', 'Power', 'Eight', 'Inside', 'Power', 'Flower', 'Seven', 'Leg', 'Power', '2019-03-08 10:47:32.173665+02', '2019-03-08 10:47:40.65706+02');
INSERT INTO public.question VALUES (167, 7, 17, '王', 'King', 'Eight', 'Inside', 'King', 'Insect', 'Seven', 'Living', 'King', '2019-03-08 10:47:41.706709+02', '2019-03-08 10:47:43.357099+02');
INSERT INTO public.question VALUES (168, 7, 18, '虫', 'Insect', 'King', 'Inside', 'Insect', 'Leg', 'Eight', 'Living', 'Insect', '2019-03-08 10:47:44.388587+02', '2019-03-08 10:47:49.573784+02');
INSERT INTO public.question VALUES (169, 7, 19, '王', 'King', 'Living', 'Seven', 'King', 'Insect', 'Power', 'Leg', 'King', '2019-03-08 10:47:50.623645+02', '2019-03-08 10:47:52.506118+02');
INSERT INTO public.question VALUES (170, 7, 20, '足', 'Leg', 'Seven', 'Two', 'Living', 'Flower', 'Power', 'Leg', 'Leg', '2019-03-08 10:47:53.539541+02', '2019-03-08 10:48:04.939294+02');
INSERT INTO public.question VALUES (171, 7, 21, '足', 'Leg', 'Insect', 'Two', 'Leg', 'Seven', 'Flower', 'Living', 'Leg', '2019-03-08 10:48:05.9898+02', '2019-03-08 10:48:11.44024+02');
INSERT INTO public.question VALUES (172, 7, 22, '二', 'Two', 'Inside', 'Two', 'Flower', 'Insect', 'King', 'Eight', 'Two', '2019-03-08 10:48:12.489534+02', '2019-03-08 10:48:15.622946+02');
INSERT INTO public.question VALUES (173, 7, 23, '七', 'Seven', 'Insect', 'King', 'Flower', 'Seven', 'Eight', 'Living', 'Seven', '2019-03-08 10:48:16.673245+02', '2019-03-08 10:48:27.756676+02');
INSERT INTO public.question VALUES (174, 7, 24, '二', 'Two', 'King', 'Inside', 'Two', 'Living', 'Power', 'Insect', 'Two', '2019-03-08 10:48:28.80636+02', '2019-03-08 10:48:31.140414+02');
INSERT INTO public.question VALUES (175, 7, 25, '二', 'Two', 'Seven', 'Insect', 'Eight', 'Flower', 'Two', 'Power', 'Two', '2019-03-08 10:48:32.189896+02', '2019-03-08 10:48:34.957026+02');
INSERT INTO public.question VALUES (176, 7, 26, '花', 'Flower', 'King', 'Inside', 'Power', 'Insect', 'Living', 'Flower', 'Flower', '2019-03-08 10:48:35.988374+02', '2019-03-08 10:48:43.223458+02');
INSERT INTO public.question VALUES (177, 7, 27, '虫', 'Insect', 'Seven', 'Living', 'Eight', 'King', 'Inside', 'Insect', 'Insect', '2019-03-08 10:48:44.272844+02', '2019-03-08 10:48:46.457119+02');
INSERT INTO public.question VALUES (178, 7, 28, '力', 'Power', 'Power', 'Inside', 'King', 'Two', 'Living', 'Flower', 'Power', '2019-03-08 10:48:47.506981+02', '2019-03-08 10:49:00.97371+02');
INSERT INTO public.question VALUES (179, 7, 29, '王', 'King', 'King', 'Insect', 'Eight', 'Two', 'Power', 'Living', 'King', '2019-03-08 10:49:02.022053+02', '2019-03-08 10:49:06.223518+02');
INSERT INTO public.question VALUES (180, 7, 30, '花', 'Flower', 'Insect', 'Flower', 'Power', 'Leg', 'Eight', 'Seven', 'Flower', '2019-03-08 10:49:07.273261+02', '2019-03-08 10:49:09.423962+02');
INSERT INTO public.question VALUES (181, 7, 31, '二', 'Two', 'Eight', 'King', 'Inside', 'Flower', 'Seven', 'Two', 'Two', '2019-03-08 10:49:10.473423+02', '2019-03-08 10:49:12.822813+02');
INSERT INTO public.question VALUES (182, 7, 32, '足', 'Leg', 'Eight', 'Flower', 'Leg', 'Power', 'Living', 'Seven', 'Leg', '2019-03-08 10:49:13.873531+02', '2019-03-08 10:49:16.27286+02');
INSERT INTO public.question VALUES (183, 7, 33, '虫', 'Insect', 'Insect', 'Living', 'Seven', 'King', 'Eight', 'Two', 'Insect', '2019-03-08 10:49:17.323335+02', '2019-03-08 10:49:19.590125+02');
INSERT INTO public.question VALUES (184, 7, 34, '花', 'Flower', 'Flower', 'Inside', 'Power', 'Two', 'Eight', 'King', 'Flower', '2019-03-08 10:49:20.639364+02', '2019-03-08 10:49:23.907069+02');
INSERT INTO public.question VALUES (185, 7, 35, '八', 'Eight', 'Eight', 'Insect', 'Leg', 'Power', 'Inside', 'King', 'Power', '2019-03-08 10:49:24.922158+02', '2019-03-08 10:49:34.190328+02');
INSERT INTO public.question VALUES (186, 7, 36, '虫', 'Insect', 'Eight', 'Inside', 'Seven', 'Insect', 'Leg', 'Two', 'Insect', '2019-03-08 10:49:35.856321+02', '2019-03-08 10:49:38.622861+02');
INSERT INTO public.question VALUES (187, 7, 37, '虫', 'Insect', 'Inside', 'King', 'Insect', 'Living', 'Eight', 'Flower', 'Insect', '2019-03-08 10:49:39.656125+02', '2019-03-08 10:49:42.207157+02');
INSERT INTO public.question VALUES (188, 7, 38, '力', 'Power', 'Power', 'Flower', 'Two', 'Eight', 'Insect', 'Seven', 'Eight', '2019-03-08 10:49:43.240132+02', '2019-03-08 10:49:45.756868+02');
INSERT INTO public.question VALUES (189, 7, 39, '足', 'Leg', 'Eight', 'Power', 'Flower', 'Two', 'Seven', 'Leg', 'Leg', '2019-03-08 10:49:50.372733+02', '2019-03-08 10:49:53.372442+02');
INSERT INTO public.question VALUES (190, 7, 40, '力', 'Power', 'Living', 'Power', 'Inside', 'Flower', 'Eight', 'Insect', 'Eight', '2019-03-08 10:49:54.42305+02', '2019-03-08 10:49:59.507084+02');
INSERT INTO public.question VALUES (191, 7, 41, '力', 'Power', 'King', 'Power', 'Seven', 'Two', 'Eight', 'Flower', 'Power', '2019-03-08 10:50:04.97273+02', '2019-03-08 10:50:07.023774+02');
INSERT INTO public.question VALUES (192, 7, 42, '花', 'Flower', 'Two', 'Seven', 'Eight', 'Leg', 'Flower', 'Power', 'Flower', '2019-03-08 10:50:08.072494+02', '2019-03-08 10:50:11.090198+02');
INSERT INTO public.question VALUES (193, 7, 43, '八', 'Eight', 'Power', 'Leg', 'Insect', 'Inside', 'Eight', 'Flower', 'Eight', '2019-03-08 10:50:12.140207+02', '2019-03-08 10:50:16.440228+02');
INSERT INTO public.question VALUES (194, 7, 44, '二', 'Two', 'Eight', 'Two', 'Seven', 'Power', 'Leg', 'Living', 'Two', '2019-03-08 10:50:17.490405+02', '2019-03-08 10:50:19.623757+02');
INSERT INTO public.question VALUES (195, 7, 45, '八', 'Eight', 'Eight', 'Insect', 'Seven', 'King', 'Power', 'Flower', 'Eight', '2019-03-08 10:50:20.67379+02', '2019-03-08 10:50:23.073714+02');
INSERT INTO public.question VALUES (196, 7, 46, '八', 'Eight', 'Eight', 'Insect', 'Leg', 'Power', 'King', 'Inside', 'Eight', '2019-03-08 10:50:24.123831+02', '2019-03-08 10:50:25.640404+02');
INSERT INTO public.question VALUES (197, 7, 47, '七', 'Seven', 'King', 'Seven', 'Living', 'Flower', 'Leg', 'Inside', 'Seven', '2019-03-08 10:50:26.690383+02', '2019-03-08 10:50:40.473846+02');
INSERT INTO public.question VALUES (198, 7, 48, '虫', 'Insect', 'Seven', 'Power', 'Insect', 'Living', 'Inside', 'King', 'Insect', '2019-03-08 10:50:41.522798+02', '2019-03-08 10:50:51.790708+02');
INSERT INTO public.question VALUES (199, 7, 49, '生', 'Living', 'Two', 'Living', 'Inside', 'Flower', 'Insect', 'Seven', 'Living', '2019-03-08 10:50:52.840746+02', '2019-03-08 10:50:55.622452+02');
INSERT INTO public.question VALUES (200, 7, 50, '力', 'Power', 'Power', 'Insect', 'Living', 'King', 'Two', 'Leg', 'Power', '2019-03-08 10:50:56.673824+02', '2019-03-08 10:51:00.656171+02');
INSERT INTO public.question VALUES (201, 7, 51, '虫', 'Insect', 'King', 'Leg', 'Insect', 'Flower', 'Living', 'Inside', 'Insect', '2019-03-08 10:51:01.706666+02', '2019-03-08 10:51:03.990447+02');
INSERT INTO public.question VALUES (202, 7, 52, '足', 'Leg', 'Two', 'Eight', 'Power', 'Leg', 'Flower', 'Inside', 'Leg', '2019-03-08 10:51:05.040204+02', '2019-03-08 10:51:07.506977+02');
INSERT INTO public.question VALUES (203, 7, 53, '八', 'Eight', 'Seven', 'Inside', 'King', 'Flower', 'Leg', 'Eight', 'Eight', '2019-03-08 10:51:08.540014+02', '2019-03-08 10:51:10.95719+02');
INSERT INTO public.question VALUES (204, 7, 54, '虫', 'Insect', 'Flower', 'King', 'Leg', 'Insect', 'Inside', 'Two', 'Insect', '2019-03-08 10:51:12.006207+02', '2019-03-08 10:51:14.773718+02');
INSERT INTO public.question VALUES (205, 7, 55, '虫', 'Insect', 'Seven', 'Eight', 'Two', 'Flower', 'Insect', 'Living', 'Insect', '2019-03-08 10:51:15.823+02', '2019-03-08 10:51:19.040384+02');
INSERT INTO public.question VALUES (206, 7, 56, '足', 'Leg', 'Living', 'Flower', 'Insect', 'Leg', 'Seven', 'Two', 'Leg', '2019-03-08 10:51:20.09018+02', '2019-03-08 10:51:22.156362+02');
INSERT INTO public.question VALUES (207, 7, 57, '力', 'Power', 'Power', 'Flower', 'King', 'Eight', 'Leg', 'Inside', 'Power', '2019-03-08 10:51:23.206801+02', '2019-03-08 10:51:25.740375+02');
INSERT INTO public.question VALUES (208, 7, 58, '八', 'Eight', 'Leg', 'Insect', 'Eight', 'Power', 'Flower', 'Seven', 'Eight', '2019-03-08 10:51:26.789212+02', '2019-03-08 10:51:29.807104+02');
INSERT INTO public.question VALUES (209, 7, 59, '虫', 'Insect', 'King', 'Power', 'Seven', 'Inside', 'Insect', 'Flower', 'Insect', '2019-03-08 10:51:30.821802+02', '2019-03-08 10:51:33.673939+02');
INSERT INTO public.question VALUES (210, 7, 60, '七', 'Seven', 'Inside', 'Seven', 'Insect', 'Leg', 'Eight', 'Flower', 'Seven', '2019-03-08 10:51:34.722808+02', '2019-03-08 10:51:40.456126+02');
INSERT INTO public.question VALUES (211, 7, 61, '花', 'Flower', 'Living', 'Seven', 'Flower', 'Two', 'Leg', 'King', 'Flower', '2019-03-08 10:51:41.505984+02', '2019-03-08 10:51:43.856105+02');
INSERT INTO public.question VALUES (212, 7, 62, '虫', 'Insect', 'Leg', 'Insect', 'Inside', 'Power', 'King', 'Two', 'Insect', '2019-03-08 10:51:44.906879+02', '2019-03-08 10:51:46.723689+02');
INSERT INTO public.question VALUES (213, 7, 63, '生', 'Living', 'Leg', 'Flower', 'Living', 'Two', 'King', 'Power', 'Living', '2019-03-08 10:51:47.772857+02', '2019-03-08 10:51:51.48923+02');
INSERT INTO public.question VALUES (214, 7, 64, '虫', 'Insect', 'Leg', 'Seven', 'Eight', 'Insect', 'Inside', 'King', 'Insect', '2019-03-08 10:51:52.540226+02', '2019-03-08 10:51:54.756873+02');
INSERT INTO public.question VALUES (215, 7, 65, '力', 'Power', 'Two', 'King', 'Power', 'Inside', 'Leg', 'Living', 'Power', '2019-03-08 10:51:55.806031+02', '2019-03-08 10:51:58.140178+02');
INSERT INTO public.question VALUES (216, 7, 66, '二', 'Two', 'Eight', 'Seven', 'Inside', 'Leg', 'Two', 'Insect', 'Two', '2019-03-08 10:51:59.190404+02', '2019-03-08 10:52:00.990131+02');
INSERT INTO public.question VALUES (217, 7, 67, '二', 'Two', 'Flower', 'Living', 'Two', 'King', 'Inside', 'Power', 'Two', '2019-03-08 10:52:02.022815+02', '2019-03-08 10:52:04.456143+02');
INSERT INTO public.question VALUES (218, 7, 68, '花', 'Flower', 'Seven', 'Leg', 'Inside', 'King', 'Eight', 'Flower', 'Flower', '2019-03-08 10:52:05.507081+02', '2019-03-08 10:52:07.573787+02');
INSERT INTO public.question VALUES (219, 7, 69, '生', 'Living', 'Living', 'King', 'Inside', 'Leg', 'Two', 'Flower', 'Living', '2019-03-08 10:52:08.623177+02', '2019-03-08 10:52:11.123809+02');
INSERT INTO public.question VALUES (220, 7, 70, '虫', 'Insect', 'Flower', 'Two', 'King', 'Insect', 'Seven', 'Leg', 'Insect', '2019-03-08 10:52:12.172657+02', '2019-03-08 10:52:14.040451+02');
INSERT INTO public.question VALUES (221, 7, 71, '二', 'Two', 'Flower', 'Two', 'Living', 'Power', 'King', 'Leg', 'Two', '2019-03-08 10:52:15.09013+02', '2019-03-08 10:52:16.773422+02');
INSERT INTO public.question VALUES (222, 7, 72, '力', 'Power', 'Power', 'Flower', 'Eight', 'Leg', 'Seven', 'King', 'Power', '2019-03-08 10:52:17.82379+02', '2019-03-08 10:52:19.606174+02');
INSERT INTO public.question VALUES (223, 7, 73, '虫', 'Insect', 'Power', 'King', 'Insect', 'Flower', 'Leg', 'Two', 'Insect', '2019-03-08 10:52:20.640063+02', '2019-03-08 10:52:22.605902+02');
INSERT INTO public.question VALUES (224, 7, 74, '二', 'Two', 'King', 'Inside', 'Power', 'Flower', 'Two', 'Living', 'Two', '2019-03-08 10:52:23.640506+02', '2019-03-08 10:52:24.990513+02');
INSERT INTO public.question VALUES (225, 7, 75, '二', 'Two', 'Seven', 'Flower', 'Leg', 'Two', 'Insect', 'Living', 'Two', '2019-03-08 10:52:26.040388+02', '2019-03-08 10:52:28.27236+02');
INSERT INTO public.question VALUES (226, 7, 76, '八', 'Eight', 'Insect', 'Living', 'Inside', 'Seven', 'Two', 'Eight', 'Eight', '2019-03-08 10:52:29.323339+02', '2019-03-08 10:52:31.206165+02');
INSERT INTO public.question VALUES (227, 7, 77, '八', 'Eight', 'King', 'Leg', 'Power', 'Seven', 'Flower', 'Eight', 'Eight', '2019-03-08 10:52:32.239389+02', '2019-03-08 10:52:34.590205+02');
INSERT INTO public.question VALUES (228, 7, 78, '八', 'Eight', 'Two', 'Power', 'Flower', 'Insect', 'Eight', 'King', 'Eight', '2019-03-08 10:52:35.640429+02', '2019-03-08 10:52:41.073769+02');
INSERT INTO public.question VALUES (229, 7, 79, '虫', 'Insect', 'Inside', 'Living', 'Two', 'Leg', 'Seven', 'Insect', 'Insect', '2019-03-08 10:52:42.123405+02', '2019-03-08 10:53:00.923766+02');
INSERT INTO public.question VALUES (230, 7, 80, '王', 'King', 'Flower', 'Seven', 'Inside', 'Eight', 'Insect', 'King', 'King', '2019-03-08 10:53:01.973842+02', '2019-03-08 10:53:04.90707+02');
INSERT INTO public.question VALUES (231, 7, 81, '力', 'Power', 'Flower', 'Two', 'Inside', 'Seven', 'Power', 'Leg', 'Power', '2019-03-08 10:53:05.940465+02', '2019-03-08 10:53:08.489354+02');
INSERT INTO public.question VALUES (232, 7, 82, '力', 'Power', 'King', 'Eight', 'Two', 'Inside', 'Seven', 'Power', 'Power', '2019-03-08 10:53:09.540378+02', '2019-03-08 10:53:13.156673+02');
INSERT INTO public.question VALUES (233, 7, 83, '力', 'Power', 'Insect', 'Living', 'King', 'Power', 'Two', 'Seven', 'Power', '2019-03-08 10:53:14.206264+02', '2019-03-08 10:53:16.590524+02');
INSERT INTO public.question VALUES (234, 7, 84, '生', 'Living', 'Eight', 'Two', 'Leg', 'Living', 'Power', 'Flower', 'Living', '2019-03-08 10:53:17.640447+02', '2019-03-08 10:53:20.607042+02');
INSERT INTO public.question VALUES (235, 7, 85, '王', 'King', 'King', 'Insect', 'Two', 'Leg', 'Seven', 'Inside', 'King', '2019-03-08 10:53:21.640373+02', '2019-03-08 10:53:23.190398+02');
INSERT INTO public.question VALUES (236, 7, 86, '虫', 'Insect', 'Insect', 'Flower', 'Inside', 'Power', 'Eight', 'Two', 'Insect', '2019-03-08 10:53:24.23932+02', '2019-03-08 10:53:27.8072+02');
INSERT INTO public.question VALUES (237, 7, 87, '八', 'Eight', 'Two', 'Living', 'Eight', 'Seven', 'Flower', 'Inside', 'Eight', '2019-03-08 10:53:28.840177+02', '2019-03-08 10:53:30.906033+02');
INSERT INTO public.question VALUES (238, 7, 88, '八', 'Eight', 'Two', 'Eight', 'Leg', 'Flower', 'King', 'Insect', 'Eight', '2019-03-08 10:53:31.940412+02', '2019-03-08 10:53:34.223681+02');
INSERT INTO public.question VALUES (239, 7, 89, '王', 'King', 'Insect', 'Power', 'Eight', 'King', 'Seven', 'Leg', 'King', '2019-03-08 10:53:35.273662+02', '2019-03-08 10:53:37.222165+02');
INSERT INTO public.question VALUES (240, 7, 90, '虫', 'Insect', 'Living', 'Power', 'Leg', 'Eight', 'Insect', 'Flower', 'Insect', '2019-03-08 10:53:38.273629+02', '2019-03-08 10:53:40.640542+02');
INSERT INTO public.question VALUES (241, 7, 91, '二', 'Two', 'Flower', 'Power', 'Eight', 'Two', 'Living', 'Seven', 'Two', '2019-03-08 10:53:41.69046+02', '2019-03-08 10:53:43.840418+02');
INSERT INTO public.question VALUES (242, 7, 92, '七', 'Seven', 'Two', 'Insect', 'Leg', 'King', 'Seven', 'Flower', 'Seven', '2019-03-08 10:53:44.872779+02', '2019-03-08 10:53:48.273559+02');
INSERT INTO public.question VALUES (243, 7, 93, '虫', 'Insect', 'Inside', 'Flower', 'Eight', 'King', 'Two', 'Insect', 'Insect', '2019-03-08 10:53:49.323835+02', '2019-03-08 10:53:51.973807+02');
INSERT INTO public.question VALUES (244, 7, 94, '花', 'Flower', 'Insect', 'Living', 'Flower', 'Seven', 'King', 'Power', 'Flower', '2019-03-08 10:53:53.023798+02', '2019-03-08 10:53:54.722893+02');
INSERT INTO public.question VALUES (245, 7, 95, '七', 'Seven', 'Inside', 'Leg', 'Insect', 'Seven', 'Two', 'Power', 'Seven', '2019-03-08 10:53:55.773742+02', '2019-03-08 10:53:57.707213+02');
INSERT INTO public.question VALUES (246, 7, 96, '八', 'Eight', 'King', 'Eight', 'Insect', 'Flower', 'Leg', 'Seven', 'Eight', '2019-03-08 10:53:58.740385+02', '2019-03-08 10:54:00.539641+02');
INSERT INTO public.question VALUES (247, 7, 97, '虫', 'Insect', 'Power', 'Insect', 'King', 'Leg', 'Flower', 'Living', 'Insect', '2019-03-08 10:54:01.590576+02', '2019-03-08 10:54:02.857237+02');
INSERT INTO public.question VALUES (248, 7, 98, '二', 'Two', 'Seven', 'King', 'Eight', 'Two', 'Leg', 'Insect', 'Two', '2019-03-08 10:54:03.907147+02', '2019-03-08 10:54:06.307077+02');
INSERT INTO public.question VALUES (249, 7, 99, '中', 'Inside', 'King', 'Insect', 'Inside', 'Leg', 'Living', 'Flower', 'Inside', '2019-03-08 10:54:07.33951+02', '2019-03-08 10:54:23.190283+02');
INSERT INTO public.question VALUES (250, 8, 0, '虫', 'Insect', 'Power', 'Two', 'Insect', 'Leg', 'Flower', 'Eight', 'Two', '2019-03-08 11:09:00.276717+02', '2019-03-08 11:09:11.175673+02');
INSERT INTO public.question VALUES (251, 8, 1, '八', 'Eight', 'Two', 'Flower', 'King', 'Insect', 'Eight', 'Inside', 'Flower', '2019-03-08 11:09:16.807871+02', '2019-03-08 11:09:20.442294+02');
INSERT INTO public.question VALUES (252, 8, 2, '中', 'Inside', 'Inside', 'Living', 'Two', 'Insect', 'Flower', 'Power', 'Two', '2019-03-08 11:09:22.691096+02', '2019-03-08 11:09:26.375678+02');
INSERT INTO public.question VALUES (253, 8, 3, '生', 'Living', 'Leg', 'Eight', 'Living', 'Seven', 'Flower', 'Two', 'Living', '2019-03-08 11:09:28.408473+02', '2019-03-08 11:09:31.925444+02');
INSERT INTO public.question VALUES (254, 8, 4, '生', 'Living', 'Living', 'Flower', 'Power', 'Insect', 'Two', 'Eight', 'Living', '2019-03-08 11:09:32.975328+02', '2019-03-08 11:09:39.325148+02');
INSERT INTO public.question VALUES (255, 8, 5, '八', 'Eight', 'Two', 'Living', 'Flower', 'Leg', 'Insect', 'Eight', 'Insect', '2019-03-08 11:09:40.375475+02', '2019-03-08 11:09:48.291982+02');
INSERT INTO public.question VALUES (256, 8, 6, '虫', 'Insect', 'Inside', 'Flower', 'Power', 'Living', 'Seven', 'Insect', 'Insect', '2019-03-08 11:09:49.724609+02', '2019-03-08 11:09:51.042249+02');
INSERT INTO public.question VALUES (257, 8, 7, '八', 'Eight', 'Leg', 'Eight', 'Two', 'Flower', 'Living', 'Insect', 'Eight', '2019-03-08 11:09:52.075485+02', '2019-03-08 11:09:54.258575+02');
INSERT INTO public.question VALUES (258, 8, 8, '虫', 'Insect', 'King', 'Power', 'Flower', 'Insect', 'Leg', 'Seven', 'Insect', '2019-03-08 11:09:55.30872+02', '2019-03-08 11:10:03.225579+02');
INSERT INTO public.question VALUES (259, 8, 9, '力', 'Power', 'Leg', 'Eight', 'Flower', 'Power', 'Inside', 'Living', 'Power', '2019-03-08 11:10:04.275312+02', '2019-03-08 11:10:08.625294+02');
INSERT INTO public.question VALUES (260, 8, 10, '中', 'Inside', 'Leg', 'Inside', 'Power', 'Eight', 'Seven', 'Insect', 'Inside', '2019-03-08 11:10:09.657602+02', '2019-03-08 11:10:12.074663+02');
INSERT INTO public.question VALUES (261, 8, 11, '八', 'Eight', 'Eight', 'Power', 'King', 'Inside', 'Insect', 'Leg', 'Eight', '2019-03-08 11:10:13.125456+02', '2019-03-08 11:10:22.359051+02');
INSERT INTO public.question VALUES (262, 8, 12, '生', 'Living', 'Inside', 'Insect', 'Living', 'King', 'Leg', 'Seven', 'Living', '2019-03-08 11:10:23.407799+02', '2019-03-08 11:10:29.792256+02');
INSERT INTO public.question VALUES (263, 8, 13, '虫', 'Insect', 'Power', 'King', 'Living', 'Two', 'Flower', 'Insect', 'Insect', '2019-03-08 11:10:30.842012+02', '2019-03-08 11:10:37.642087+02');
INSERT INTO public.question VALUES (264, 8, 14, '王', 'King', 'Living', 'King', 'Leg', 'Eight', 'Seven', 'Inside', 'King', '2019-03-08 11:10:38.67483+02', '2019-03-08 11:10:41.291688+02');
INSERT INTO public.question VALUES (265, 8, 15, '花', 'Flower', 'Flower', 'Seven', 'Leg', 'Two', 'Eight', 'Power', 'Leg', '2019-03-08 11:10:42.34232+02', '2019-03-08 11:10:49.909073+02');
INSERT INTO public.question VALUES (266, 8, 16, '力', 'Power', 'Eight', 'Inside', 'Power', 'Flower', 'Seven', 'Leg', 'Eight', '2019-03-08 11:10:53.175674+02', '2019-03-08 11:10:53.409175+02');
INSERT INTO public.question VALUES (267, 8, 17, '王', 'King', 'Eight', 'Inside', 'King', 'Insect', 'Seven', 'Living', 'King', '2019-03-08 11:10:55.575634+02', '2019-03-08 11:10:58.708098+02');
INSERT INTO public.question VALUES (268, 8, 18, '虫', 'Insect', 'King', 'Inside', 'Insect', 'Leg', 'Eight', 'Living', 'Insect', '2019-03-08 11:10:59.759167+02', '2019-03-08 11:11:01.52573+02');
INSERT INTO public.question VALUES (269, 8, 19, '王', 'King', 'Living', 'Seven', 'King', 'Insect', 'Power', 'Leg', 'King', '2019-03-08 11:11:02.575583+02', '2019-03-08 11:11:04.15904+02');
INSERT INTO public.question VALUES (270, 8, 20, '足', 'Leg', 'Seven', 'Two', 'Living', 'Flower', 'Power', 'Leg', 'Power', '2019-03-08 11:11:05.20801+02', '2019-03-08 11:11:10.425821+02');
INSERT INTO public.question VALUES (271, 8, 21, '足', 'Leg', 'Insect', 'Two', 'Leg', 'Seven', 'Flower', 'Living', 'Leg', '2019-03-08 11:11:11.675555+02', '2019-03-08 11:11:14.109107+02');
INSERT INTO public.question VALUES (272, 8, 22, '二', 'Two', 'Inside', 'Two', 'Flower', 'Insect', 'King', 'Eight', 'Two', '2019-03-08 11:11:15.159137+02', '2019-03-08 11:11:19.142637+02');
INSERT INTO public.question VALUES (273, 8, 23, '七', 'Seven', 'Insect', 'King', 'Flower', 'Seven', 'Eight', 'Living', 'Seven', '2019-03-08 11:11:20.175396+02', '2019-03-08 11:11:25.425565+02');
INSERT INTO public.question VALUES (274, 8, 24, '二', 'Two', 'King', 'Inside', 'Two', 'Living', 'Power', 'Insect', 'Two', '2019-03-08 11:11:26.475523+02', '2019-03-08 11:11:28.408447+02');
INSERT INTO public.question VALUES (275, 8, 25, '二', 'Two', 'Seven', 'Insect', 'Eight', 'Flower', 'Two', 'Power', 'Two', '2019-03-08 11:11:29.459004+02', '2019-03-08 11:11:32.608979+02');
INSERT INTO public.question VALUES (276, 8, 26, '花', 'Flower', 'King', 'Inside', 'Power', 'Insect', 'Living', 'Flower', 'Flower', '2019-03-08 11:11:33.659205+02', '2019-03-08 11:11:46.424751+02');
INSERT INTO public.question VALUES (277, 8, 27, '虫', 'Insect', 'Seven', 'Living', 'Eight', 'King', 'Inside', 'Insect', 'Insect', '2019-03-08 11:11:47.475018+02', '2019-03-08 11:11:49.692581+02');
INSERT INTO public.question VALUES (278, 8, 28, '力', 'Power', 'Power', 'Inside', 'King', 'Two', 'Living', 'Flower', 'Flower', '2019-03-08 11:11:50.742657+02', '2019-03-08 11:11:55.326019+02');
INSERT INTO public.question VALUES (279, 8, 29, '王', 'King', 'King', 'Insect', 'Eight', 'Two', 'Power', 'Living', 'King', '2019-03-08 11:11:57.191407+02', '2019-03-08 11:12:00.490575+02');
INSERT INTO public.question VALUES (280, 8, 30, '花', 'Flower', 'Insect', 'Flower', 'Power', 'Leg', 'Eight', 'Seven', 'Flower', '2019-03-08 11:12:01.54102+02', '2019-03-08 11:12:03.308625+02');
INSERT INTO public.question VALUES (281, 8, 31, '二', 'Two', 'Eight', 'King', 'Inside', 'Flower', 'Seven', 'Two', 'Two', '2019-03-08 11:12:04.358294+02', '2019-03-08 11:12:07.042613+02');
INSERT INTO public.question VALUES (282, 8, 32, '足', 'Leg', 'Eight', 'Flower', 'Leg', 'Power', 'Living', 'Seven', 'Living', '2019-03-08 11:12:08.075297+02', '2019-03-08 11:12:15.508953+02');
INSERT INTO public.question VALUES (283, 8, 33, '虫', 'Insect', 'Insect', 'Living', 'Seven', 'King', 'Eight', 'Two', 'Insect', '2019-03-08 11:12:16.908214+02', '2019-03-08 11:12:20.925383+02');
INSERT INTO public.question VALUES (284, 8, 34, '花', 'Flower', 'Flower', 'Inside', 'Power', 'Two', 'Eight', 'King', 'Flower', '2019-03-08 11:12:21.97595+02', '2019-03-08 11:12:23.858699+02');
INSERT INTO public.question VALUES (285, 8, 35, '八', 'Eight', 'Eight', 'Insect', 'Leg', 'Power', 'Inside', 'King', 'Eight', '2019-03-08 11:12:24.908309+02', '2019-03-08 11:12:30.959303+02');
INSERT INTO public.question VALUES (286, 8, 36, '虫', 'Insect', 'Eight', 'Inside', 'Seven', 'Insect', 'Leg', 'Two', 'Insect', '2019-03-08 11:12:32.009287+02', '2019-03-08 11:12:39.624938+02');
INSERT INTO public.question VALUES (287, 8, 37, '虫', 'Insect', 'Inside', 'King', 'Insect', 'Living', 'Eight', 'Flower', 'Insect', '2019-03-08 11:12:40.675306+02', '2019-03-08 11:12:44.042318+02');
INSERT INTO public.question VALUES (288, 8, 38, '力', 'Power', 'Power', 'Flower', 'Two', 'Eight', 'Insect', 'Seven', 'Power', '2019-03-08 11:12:45.075147+02', '2019-03-08 11:12:51.409072+02');
INSERT INTO public.question VALUES (289, 8, 39, '足', 'Leg', 'Eight', 'Power', 'Flower', 'Two', 'Seven', 'Leg', 'Leg', '2019-03-08 11:12:52.458977+02', '2019-03-08 11:13:00.526124+02');
INSERT INTO public.question VALUES (290, 8, 40, '力', 'Power', 'Living', 'Power', 'Inside', 'Flower', 'Eight', 'Insect', 'Power', '2019-03-08 11:13:01.575232+02', '2019-03-08 11:13:05.642653+02');
INSERT INTO public.question VALUES (291, 8, 41, '力', 'Power', 'King', 'Power', 'Seven', 'Two', 'Eight', 'Flower', 'Power', '2019-03-08 11:13:06.675914+02', '2019-03-08 11:13:07.792583+02');
INSERT INTO public.question VALUES (292, 8, 42, '花', 'Flower', 'Two', 'Seven', 'Eight', 'Leg', 'Flower', 'Power', 'Flower', '2019-03-08 11:13:08.842306+02', '2019-03-08 11:13:11.025951+02');
INSERT INTO public.question VALUES (293, 8, 43, '八', 'Eight', 'Power', 'Leg', 'Insect', 'Inside', 'Eight', 'Flower', 'Insect', '2019-03-08 11:13:12.075074+02', '2019-03-08 11:13:16.025148+02');
INSERT INTO public.question VALUES (294, 8, 44, '二', 'Two', 'Eight', 'Two', 'Seven', 'Power', 'Leg', 'Living', 'Two', '2019-03-08 11:13:18.174717+02', '2019-03-08 11:13:19.94221+02');
INSERT INTO public.question VALUES (295, 8, 45, '八', 'Eight', 'Eight', 'Insect', 'Seven', 'King', 'Power', 'Flower', 'Eight', '2019-03-08 11:13:20.975372+02', '2019-03-08 11:13:25.242731+02');
INSERT INTO public.question VALUES (296, 8, 46, '八', 'Eight', 'Eight', 'Insect', 'Leg', 'Power', 'King', 'Inside', 'Eight', '2019-03-08 11:13:26.275893+02', '2019-03-08 11:13:28.525957+02');
INSERT INTO public.question VALUES (297, 8, 47, '七', 'Seven', 'King', 'Seven', 'Living', 'Flower', 'Leg', 'Inside', 'Leg', '2019-03-08 11:13:29.575969+02', '2019-03-08 11:13:32.959084+02');
INSERT INTO public.question VALUES (298, 8, 48, '虫', 'Insect', 'Seven', 'Power', 'Insect', 'Living', 'Inside', 'King', 'Insect', '2019-03-08 11:13:35.191922+02', '2019-03-08 11:13:37.109263+02');
INSERT INTO public.question VALUES (299, 8, 49, '生', 'Living', 'Two', 'Living', 'Inside', 'Flower', 'Insect', 'Seven', 'Living', '2019-03-08 11:13:38.158863+02', '2019-03-08 11:13:45.475977+02');
INSERT INTO public.question VALUES (300, 8, 50, '力', 'Power', 'Power', 'Insect', 'Living', 'King', 'Two', 'Leg', 'Power', '2019-03-08 11:13:46.525978+02', '2019-03-08 11:13:49.292617+02');
INSERT INTO public.question VALUES (301, 8, 51, '虫', 'Insect', 'King', 'Leg', 'Insect', 'Flower', 'Living', 'Inside', 'Insect', '2019-03-08 11:13:50.34159+02', '2019-03-08 11:13:55.591486+02');
INSERT INTO public.question VALUES (302, 8, 52, '足', 'Leg', 'Two', 'Eight', 'Power', 'Leg', 'Flower', 'Inside', 'Leg', '2019-03-08 11:13:56.642551+02', '2019-03-08 11:14:01.242482+02');
INSERT INTO public.question VALUES (303, 8, 53, '八', 'Eight', 'Seven', 'Inside', 'King', 'Flower', 'Leg', 'Eight', 'Eight', '2019-03-08 11:14:02.276046+02', '2019-03-08 11:14:05.776072+02');
INSERT INTO public.question VALUES (304, 8, 54, '虫', 'Insect', 'Flower', 'King', 'Leg', 'Insect', 'Inside', 'Two', 'Leg', '2019-03-08 11:14:06.825713+02', '2019-03-08 11:14:09.509107+02');
INSERT INTO public.question VALUES (305, 8, 55, '虫', 'Insect', 'Seven', 'Eight', 'Two', 'Flower', 'Insect', 'Living', 'Insect', '2019-03-08 11:14:11.309439+02', '2019-03-08 11:14:14.609056+02');
INSERT INTO public.question VALUES (306, 8, 56, '足', 'Leg', 'Living', 'Flower', 'Insect', 'Leg', 'Seven', 'Two', 'Leg', '2019-03-08 11:14:15.658442+02', '2019-03-08 11:14:18.092853+02');
INSERT INTO public.question VALUES (307, 8, 57, '力', 'Power', 'Power', 'Flower', 'King', 'Eight', 'Leg', 'Inside', 'Power', '2019-03-08 11:14:19.14144+02', '2019-03-08 11:14:20.792754+02');
INSERT INTO public.question VALUES (308, 8, 58, '八', 'Eight', 'Leg', 'Insect', 'Eight', 'Power', 'Flower', 'Seven', 'Eight', '2019-03-08 11:14:21.842978+02', '2019-03-08 11:14:24.391697+02');
INSERT INTO public.question VALUES (309, 8, 59, '虫', 'Insect', 'King', 'Power', 'Seven', 'Inside', 'Insect', 'Flower', 'Insect', '2019-03-08 11:14:25.442676+02', '2019-03-08 11:14:27.908826+02');
INSERT INTO public.question VALUES (310, 8, 60, '七', 'Seven', 'Inside', 'Seven', 'Insect', 'Leg', 'Eight', 'Flower', 'Seven', '2019-03-08 11:14:28.958315+02', '2019-03-08 11:14:33.941728+02');
INSERT INTO public.question VALUES (311, 8, 61, '花', 'Flower', 'Living', 'Seven', 'Flower', 'Two', 'Leg', 'King', 'Flower', '2019-03-08 11:14:34.974995+02', '2019-03-08 11:14:38.041962+02');
INSERT INTO public.question VALUES (312, 8, 62, '虫', 'Insect', 'Leg', 'Insect', 'Inside', 'Power', 'King', 'Two', 'Insect', '2019-03-08 11:14:39.075354+02', '2019-03-08 11:14:41.759318+02');
INSERT INTO public.question VALUES (313, 8, 63, '生', 'Living', 'Leg', 'Flower', 'Living', 'Two', 'King', 'Power', 'King', '2019-03-08 11:14:42.809392+02', '2019-03-08 11:14:48.109348+02');
INSERT INTO public.question VALUES (314, 8, 64, '虫', 'Insect', 'Leg', 'Seven', 'Eight', 'Insect', 'Inside', 'King', 'Insect', '2019-03-08 11:14:49.375771+02', '2019-03-08 11:14:51.142692+02');
INSERT INTO public.question VALUES (315, 8, 65, '力', 'Power', 'Two', 'King', 'Power', 'Inside', 'Leg', 'Living', 'Power', '2019-03-08 11:14:52.17627+02', '2019-03-08 11:14:54.5593+02');
INSERT INTO public.question VALUES (316, 8, 66, '二', 'Two', 'Eight', 'Seven', 'Inside', 'Leg', 'Two', 'Insect', 'Two', '2019-03-08 11:14:55.607293+02', '2019-03-08 11:14:57.159149+02');
INSERT INTO public.question VALUES (317, 8, 67, '二', 'Two', 'Flower', 'Living', 'Two', 'King', 'Inside', 'Power', 'Two', '2019-03-08 11:14:58.209172+02', '2019-03-08 11:15:00.325023+02');
INSERT INTO public.question VALUES (318, 8, 68, '花', 'Flower', 'Seven', 'Leg', 'Inside', 'King', 'Eight', 'Flower', 'Flower', '2019-03-08 11:15:01.357938+02', '2019-03-08 11:15:03.209396+02');
INSERT INTO public.question VALUES (319, 8, 69, '生', 'Living', 'Living', 'King', 'Inside', 'Leg', 'Two', 'Flower', 'Living', '2019-03-08 11:15:04.258456+02', '2019-03-08 11:15:08.892688+02');
INSERT INTO public.question VALUES (320, 8, 70, '虫', 'Insect', 'Flower', 'Two', 'King', 'Insect', 'Seven', 'Leg', 'Insect', '2019-03-08 11:15:09.942311+02', '2019-03-08 11:15:11.876242+02');
INSERT INTO public.question VALUES (321, 8, 71, '二', 'Two', 'Flower', 'Two', 'Living', 'Power', 'King', 'Leg', 'Two', '2019-03-08 11:15:12.92599+02', '2019-03-08 11:15:14.09269+02');
INSERT INTO public.question VALUES (322, 8, 72, '力', 'Power', 'Power', 'Flower', 'Eight', 'Leg', 'Seven', 'King', 'Power', '2019-03-08 11:15:15.14256+02', '2019-03-08 11:15:16.441325+02');
INSERT INTO public.question VALUES (323, 8, 73, '虫', 'Insect', 'Power', 'King', 'Insect', 'Flower', 'Leg', 'Two', 'Insect', '2019-03-08 11:15:17.474663+02', '2019-03-08 11:15:19.742591+02');
INSERT INTO public.question VALUES (324, 8, 74, '二', 'Two', 'King', 'Inside', 'Power', 'Flower', 'Two', 'Living', 'Two', '2019-03-08 11:15:20.775461+02', '2019-03-08 11:15:22.459184+02');
INSERT INTO public.question VALUES (325, 8, 75, '二', 'Two', 'Seven', 'Flower', 'Leg', 'Two', 'Insect', 'Living', 'Two', '2019-03-08 11:15:23.508487+02', '2019-03-08 11:15:25.992361+02');
INSERT INTO public.question VALUES (326, 8, 76, '八', 'Eight', 'Insect', 'Living', 'Inside', 'Seven', 'Two', 'Eight', 'Eight', '2019-03-08 11:15:27.042601+02', '2019-03-08 11:15:28.740956+02');
INSERT INTO public.question VALUES (327, 8, 77, '八', 'Eight', 'King', 'Leg', 'Power', 'Seven', 'Flower', 'Eight', 'Eight', '2019-03-08 11:15:29.774078+02', '2019-03-08 11:15:31.208508+02');
INSERT INTO public.question VALUES (328, 8, 78, '八', 'Eight', 'Two', 'Power', 'Flower', 'Insect', 'Eight', 'King', 'Eight', '2019-03-08 11:15:32.25856+02', '2019-03-08 11:15:34.675438+02');
INSERT INTO public.question VALUES (329, 8, 79, '虫', 'Insect', 'Inside', 'Living', 'Two', 'Leg', 'Seven', 'Insect', 'Insect', '2019-03-08 11:15:35.725483+02', '2019-03-08 11:15:38.875416+02');
INSERT INTO public.question VALUES (330, 8, 80, '王', 'King', 'Flower', 'Seven', 'Inside', 'Eight', 'Insect', 'King', 'King', '2019-03-08 11:15:39.924963+02', '2019-03-08 11:15:42.191622+02');
INSERT INTO public.question VALUES (331, 8, 81, '力', 'Power', 'Flower', 'Two', 'Inside', 'Seven', 'Power', 'Leg', 'Power', '2019-03-08 11:15:43.242415+02', '2019-03-08 11:15:45.175055+02');
INSERT INTO public.question VALUES (332, 8, 82, '力', 'Power', 'King', 'Eight', 'Two', 'Inside', 'Seven', 'Power', 'Power', '2019-03-08 11:15:46.224858+02', '2019-03-08 11:15:48.17537+02');
INSERT INTO public.question VALUES (333, 8, 83, '力', 'Power', 'Insect', 'Living', 'King', 'Power', 'Two', 'Seven', 'Power', '2019-03-08 11:15:49.224162+02', '2019-03-08 11:15:51.17526+02');
INSERT INTO public.question VALUES (334, 8, 84, '生', 'Living', 'Eight', 'Two', 'Leg', 'Living', 'Power', 'Flower', 'Living', '2019-03-08 11:15:52.225148+02', '2019-03-08 11:15:57.375032+02');
INSERT INTO public.question VALUES (335, 8, 85, '王', 'King', 'King', 'Insect', 'Two', 'Leg', 'Seven', 'Inside', 'King', '2019-03-08 11:15:58.425096+02', '2019-03-08 11:16:00.658592+02');
INSERT INTO public.question VALUES (336, 8, 86, '虫', 'Insect', 'Insect', 'Flower', 'Inside', 'Power', 'Eight', 'Two', 'Insect', '2019-03-08 11:16:01.70961+02', '2019-03-08 11:16:03.458369+02');
INSERT INTO public.question VALUES (337, 8, 87, '八', 'Eight', 'Two', 'Living', 'Eight', 'Seven', 'Flower', 'Inside', 'Eight', '2019-03-08 11:16:04.507998+02', '2019-03-08 11:16:06.108618+02');
INSERT INTO public.question VALUES (338, 8, 88, '八', 'Eight', 'Two', 'Eight', 'Leg', 'Flower', 'King', 'Insect', 'Eight', '2019-03-08 11:16:07.159368+02', '2019-03-08 11:16:08.792899+02');
INSERT INTO public.question VALUES (339, 8, 89, '王', 'King', 'Insect', 'Power', 'Eight', 'King', 'Seven', 'Leg', 'King', '2019-03-08 11:16:09.842444+02', '2019-03-08 11:16:14.85757+02');
INSERT INTO public.question VALUES (340, 8, 90, '虫', 'Insect', 'Living', 'Power', 'Leg', 'Eight', 'Insect', 'Flower', 'Insect', '2019-03-08 11:16:15.908969+02', '2019-03-08 11:16:17.82547+02');
INSERT INTO public.question VALUES (341, 8, 91, '二', 'Two', 'Flower', 'Power', 'Eight', 'Two', 'Living', 'Seven', 'Two', '2019-03-08 11:16:18.87515+02', '2019-03-08 11:16:22.124625+02');
INSERT INTO public.question VALUES (342, 8, 92, '七', 'Seven', 'Two', 'Insect', 'Leg', 'King', 'Seven', 'Flower', 'Seven', '2019-03-08 11:16:23.174118+02', '2019-03-08 11:16:25.3913+02');
INSERT INTO public.question VALUES (343, 8, 93, '虫', 'Insect', 'Inside', 'Flower', 'Eight', 'King', 'Two', 'Insect', 'Insect', '2019-03-08 11:16:26.441303+02', '2019-03-08 11:16:28.641548+02');
INSERT INTO public.question VALUES (344, 8, 94, '花', 'Flower', 'Insect', 'Living', 'Flower', 'Seven', 'King', 'Power', 'Flower', '2019-03-08 11:16:29.674886+02', '2019-03-08 11:16:32.108931+02');
INSERT INTO public.question VALUES (345, 8, 95, '七', 'Seven', 'Inside', 'Leg', 'Insect', 'Seven', 'Two', 'Power', 'Seven', '2019-03-08 11:16:33.158099+02', '2019-03-08 11:16:35.158651+02');
INSERT INTO public.question VALUES (346, 8, 96, '八', 'Eight', 'King', 'Eight', 'Insect', 'Flower', 'Leg', 'Seven', 'Eight', '2019-03-08 11:16:36.208115+02', '2019-03-08 11:16:37.491735+02');
INSERT INTO public.question VALUES (347, 8, 97, '虫', 'Insect', 'Power', 'Insect', 'King', 'Leg', 'Flower', 'Living', 'Insect', '2019-03-08 11:16:38.541571+02', '2019-03-08 11:16:41.558308+02');
INSERT INTO public.question VALUES (348, 8, 98, '二', 'Two', 'Seven', 'King', 'Eight', 'Two', 'Leg', 'Insect', 'Two', '2019-03-08 11:16:42.607923+02', '2019-03-08 11:16:44.142286+02');
INSERT INTO public.question VALUES (349, 8, 99, '中', 'Inside', 'King', 'Insect', 'Inside', 'Leg', 'Living', 'Flower', 'Inside', '2019-03-08 11:16:45.17495+02', '2019-03-08 11:16:47.274997+02');


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public."user" VALUES (6, '2019-03-08 10:12:54.477201+02');
INSERT INTO public."user" VALUES (7, '2019-03-08 10:45:34.382527+02');
INSERT INTO public."user" VALUES (8, '2019-03-08 11:09:00.25473+02');


--
-- Name: question_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.question_id_seq', 349, true);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_id_seq', 8, true);


--
-- PostgreSQL database dump complete
--

