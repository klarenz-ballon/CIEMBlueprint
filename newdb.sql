CREATE TABLE committee(
    comm_id SERIAL PRIMARY KEY not null,
    comm_name varchar(256) not null,
    comm_delete_ind bool default false not null
);

INSERT INTO committee(comm_name) VALUES
('Academic Affairs Committee'),
('External Affairs Committee'),
('Finance Committee'),
('Internal Affairs Committee'),
('Membership and Recruitment Committee'),
('Publications and Records Committee');


CREATE TABLE headship ( 
head_id SERIAL PRIMARY KEY not null, 
head_name VARCHAR(512) not null, 
head_delete_ind BOOLEAN default false not null
);

INSERT INTO headship(head_name) VALUES
('Committee Director'),
('Project Executive Head'),
('Project Committee Head'),
('Project Member');


CREATE TABLE specialization (
spec_id SERIAL PRIMARY KEY not null,
spec_name VARCHAR(100) not null,
spec_delete_ind BOOLEAN DEFAULT FALSE NOT NULL
);

INSERT INTO specialization(spec_name) VALUES
('Operations Research'),
('Supply Chain Management'),
('Ergonomics'),
('Information Technology'),
('Quality Control'),
('Finance'),
('Industrial Design'),
('Academe'),
('Others');

-- Table: Degree
CREATE TABLE degree (
degree_id SERIAL PRIMARY KEY,
degree_name VARCHAR(256) not null,
degree_delete_ind BOOLEAN DEFAULT FALSE NOT NULL
);

INSERT INTO degree(degree_name) VALUES
('BS Industrial Engineering'),
('BS Chemical Engineering'),
('BS Civil Engineering'),
('BS Computer Science'),
('BS Computer Engineering'),
('BS Electronics Engineering'),
('BS Electrical Engineering'),
('BS Geodetic Engineering'),
('BS Mechanical Engineering'),
('BS Materials Engineering'),
('BS Metallurgical Engineering'),
('BS Mining Engineering');

-- Table: App Batch
CREATE TABLE appbatch (
appbatch_id SERIAL PRIMARY KEY,
appbatch_name VARCHAR(3) not null,
appbatch_delete_ind BOOLEAN DEFAULT FALSE NOT NULL
);

INSERT INTO appbatch(appbatch_name) VALUES
('23B'),
('23A'),
('22B'),
('22A'),
('21B'),
('21A'),
('20B'),
('20A'),
('19B'),
('19A');

-- Table: User
CREATE TABLE admin (
    admin_id SERIAL PRIMARY KEY NOT NULL,
    admin_name VARCHAR(100) NOT NULL,
    admin_pass VARCHAR(100) NOT NULL,
    admin_delete_ind BOOLEAN DEFAULT FALSE NOT NULL
);

INSERT INTO admin (admin_name, admin_pass, admin_delete_ind) 
VALUES ('ciem1976', 'CIEMBak1976', FALSE);

-- Table: Status
CREATE TABLE status (
status_id SERIAL PRIMARY KEY not null,
status_name VARCHAR(50) not null,
status_delete_ind BOOLEAN DEFAULT FALSE NOT NULL
);

INSERT INTO status(status_name) VALUES
('Active'),
('Inactive');

-- Table: Memtype
CREATE TABLE memtype (
memtype_id SERIAL PRIMARY KEY not null,
memtype_name VARCHAR(50) not null,
memtype_delete_ind BOOLEAN DEFAULT FALSE NOT NULL
);

INSERT INTO memtype(memtype_name) VALUES
('Regular'),
('Non-Regular'),
('Honorary'),
('Probationary');

-- Table: Member
CREATE TABLE member (
mem_id SERIAL PRIMARY KEY not null,
mem_fn VARCHAR(100) not null,
mem_mn VARCHAR(100),
mem_ln VARCHAR(100) not null,
mem_sf VARCHAR(5),
mem_st_num VARCHAR(9) not null,
mem_bd DATE not null,
mem_cn VARCHAR(11) not null,
mem_emergency VARCHAR(11) not null,
mem_email VARCHAR(50) not null,
mem_up_email VARCHAR(50) not null,
mem_pres_add VARCHAR(512) not null,
mem_perma_add VARCHAR(512) not null,
mem_year_batch VARCHAR(20) not null,
mem_year_standing INTEGER not null,
degree_id INTEGER NOT NULL not null,
mem_other_org VARCHAR(512) not null,
status_id INTEGER NOT NULL not null,
memtype_id INTEGER NOT NULL not null,
mem_reaffiliated BOOLEAN not null,
mem_is_new BOOLEAN not null,
appbatch_id integer,	
mem_delete_ind BOOLEAN DEFAULT FALSE NOT NULL,
CONSTRAINT appbatch_id_fkey FOREIGN KEY (appbatch_id) 
REFERENCES  appbatch(appbatch_id),
CONSTRAINT degree_id_fkey FOREIGN KEY (degree_id) 
REFERENCES  degree(degree_id),
CONSTRAINT status_id_fkey FOREIGN KEY (status_id) 
REFERENCES status(status_id),
CONSTRAINT memtype_id_fkey FOREIGN KEY (memtype_id) 
REFERENCES memtype(memtype_id)
);

INSERT INTO member (mem_fn, mem_mn, mem_ln, mem_sf, mem_st_num, mem_bd, mem_cn, mem_emergency, mem_email, mem_up_email, mem_pres_add, mem_perma_add, mem_year_batch, appbatch_id, mem_year_standing, degree_id, mem_other_org, status_id, memtype_id, mem_reaffiliated, mem_is_new, mem_delete_ind) 
VALUES
('Emily', 'Grace', 'Smith', null, '202400001', '1990-06-15', '09123456789', '09543210987', 'example123@gmail.com', 'john.doe@up.edu.ph', 'Unit 101, Acacia Residences, Makati City, Metro Manila', 'Block 7, Lot 12, Phase 3, Villa Caceres Subdivision, Bacolod City, Negros Occidental', 2017, 4, 3, 1, 'UP CIEM', 1, 3, TRUE, TRUE, FALSE),
('James', 'Alexander', 'Johnson', null, '201900123', '1995-03-25', '09987654321', '09876543210', 'john.doe567@yahoo.com', 'emily.smith@up.edu.ph', 'Block 3, Lot 5, Phase 2, BF Homes, Parañaque City, Metro Manila', 'Unit 301, Tower 1, Acacia Estates, Taguig City, Metro Manila', 2018, 4, 1, 2, 'IEC', 2, 4, FALSE, FALSE, FALSE),
('Sophia', '', 'Brown', 'III', '202310002', '1999-11-10', '09456789012', '09123456780', 'emily.smith789@hotmail.com', 'james.brown@up.edu.ph', 'Barangay San Antonio, Quezon City, Metro Manila', 'Purok Masagana, Brgy. San Isidro, Cagayan de Oro City, Misamis Oriental', 2019, 4, 5, 3, 'N/A', 1, 1, TRUE, TRUE, FALSE),
('Liam', 'Michael', 'Davis', null, '202210345', '2000-09-05', '09765432109', '09789012345', 'jackson.wang456@outlook.com', 'sophia.jones@up.edu.ph', 'Purok 2, Brgy. Poblacion, Davao City, Davao del Sur', 'Phase 2, Block 5, Lot 8, Villa de Mercedes, Davao City, Davao del Sur', 2020, 4, 2, 1, 'GEOP', 2, 2, FALSE, FALSE, FALSE),
('Olivia', 'Elizabeth', 'Wilson', null, '202510678', '2002-01-30', '09234567890', '09432109876', 'sarah.jones321@live.com', 'michael.nguyen@up.edu.ph', 'Lot 15, Phase 1, Northcrest Subdivision, Bacolod City, Negros Occidental', 'Blk 10, Lot 15, Kingsville Hills Subdivision, Antipolo City, Rizal', 2021, 2, 4, 2, 'IEC, CSA', 1, 3, TRUE, TRUE, FALSE);

CREATE TABLE reaffiliation(
    reaff_id SERIAL PRIMARY KEY not null,
    reaff_date date default current_date,
    reaff_sem varchar(50) not null,
    reaff_gwa VARCHAR(10) not null,
    reaff_acad_year varchar(100) not null,
    reaff_choice1 integer,
    reaff_choice2 integer,
    reaff_choice3 integer,
    reaff_choice4 integer,
    reaff_choice5 integer,
    reaff_choice6 integer,
    reaff_assigned_comm integer,
    reaff_is_new bool NOT NULL,
    reaff_is_paid bool default false not null,
    reaff_date_paid date,
    reaff_delete_ind bool default false not null,
    mem_id int not null,
    CONSTRAINT reaffiliation_choice1_id_fkey FOREIGN KEY (reaff_choice1) REFERENCES committee(comm_id),
    CONSTRAINT reaffiliation_choice2_id_fkey FOREIGN KEY (reaff_choice2) REFERENCES committee(comm_id),
    CONSTRAINT reaffiliation_choice3_id_fkey FOREIGN KEY (reaff_choice3) REFERENCES committee(comm_id),
    CONSTRAINT reaffiliation_choice4_id_fkey FOREIGN KEY (reaff_choice4) REFERENCES committee(comm_id),
    CONSTRAINT reaffiliation_choice5_id_fkey FOREIGN KEY (reaff_choice5) REFERENCES committee(comm_id),
    CONSTRAINT reaffiliation_choice6_id_fkey FOREIGN KEY (reaff_choice6) REFERENCES committee(comm_id),
    CONSTRAINT reaffiliation_assigned_comm_id_fkey FOREIGN KEY (reaff_assigned_comm) REFERENCES committee(comm_id),
    CONSTRAINT reaffiliation_mem_id_fkey FOREIGN KEY (mem_id) REFERENCES member(mem_id)
);

INSERT INTO reaffiliation (reaff_is_new, reaff_date, reaff_sem, reaff_acad_year, reaff_choice1, reaff_choice2, reaff_choice3, reaff_choice4, reaff_choice5, reaff_choice6, reaff_is_paid, reaff_date_paid, reaff_delete_ind, mem_id, reaff_gwa,reaff_assigned_comm)
VALUES
(TRUE, '2020-06-01', '1st', '2020-2021', 4, 5, 2, 6, 3, 1, TRUE, '2020-01-01', FALSE, 1, 1.00,1),
(TRUE, '2021-06-15', '1st', '2021-2022', 3, 6, 2, 5, 1, 4, FALSE, '2021-07-15', FALSE, 2, 1.75,2),
(TRUE, '2022-06-30', '1st', '2022-2023', 6, 5, 1, 4, 3, 2, FALSE, '2022-10-30', FALSE, 3, 2.345,4),
(TRUE, '2023-06-25', '1st', '2023-2024', 2, 5, 3, 1, 4, 6, TRUE, '2023-12-15', FALSE, 4, 2.125,4),
(TRUE, '2023-06-10', '1st', '2023-2024', 4, 1, 3, 6, 2, 5, FALSE, '2024-12-31', FALSE, 5, 1.9875,6),
(FALSE, '2021-01-01', '2nd', '2020-2021', 4, 5, 2, 6, 3, 1, TRUE, '2021-01-01', FALSE, 1, 1.22,1),
(FALSE, '2022-01-15', '2nd', '2021-2022', 3, 6, 2, 5, 1, 4, FALSE, '2022-07-15', FALSE, 2, 1.45,2),
(FALSE, '2023-01-30', '2nd', '2022-2023', 6, 5, 1, 4, 3, 2, FALSE, '2023-10-30', FALSE, 3, 1.345,3),
(FALSE, '2024-01-25', '2nd', '2023-2024', 2, 5, 3, 1, 4, 6, TRUE, '2024-12-15', FALSE, 4, 1.1534,5),
(FALSE, '2024-01-10', '2nd', '2023-2024', 4, 1, 3, 6, 2, 5, FALSE, '2024-12-31', FALSE, 5, 1.8705,6);


-- Table: Headship_Score
CREATE TABLE headship_score (
    mem_id INTEGER NOT NULL,
    head_id INTEGER NOT NULL,
    headscore_description VARCHAR(512)  not null,
    headscore_acad_year varchar(100) not null,
    headscore_score INTEGER not null,
    headscore_delete_ind BOOLEAN DEFAULT FALSE NOT NULL,
    CONSTRAINT mem_id_fkey FOREIGN KEY (mem_id) REFERENCES member(mem_id),
    CONSTRAINT head_id_fkey FOREIGN KEY (head_id) REFERENCES headship(head_id)
);

INSERT INTO headship_score(mem_id, head_id, headscore_description, headscore_acad_year, headscore_score, headscore_delete_ind) VALUES

(1, 1, 'Director for Academic Welfare', '2022-2023', 10, FALSE),
(2, 2, 'EPM Ieshikawa', '2019-2020', 8, FALSE),
(3, 3, 'Programs Manager Ieshikawa', '2020-2021', 5, FALSE),
(4, 4, 'FART Member', '2023-2024', 2, FALSE),
(5, 1, 'Director for Membership Evaluation', '2018-2019', 10, FALSE);

-- Table: Alumni
CREATE TABLE alumni (
alum_id SERIAL PRIMARY KEY,
alum_fn VARCHAR(100) NOT NULL,
alum_mn VARCHAR(100),
alum_ln VARCHAR(100) NOT NULL,
alum_sf VARCHAR(6),
alum_st_num VARCHAR(9) NOT NULL,
alum_cn VARCHAR(11) NOT NULL,
alum_email VARCHAR(100) NOT NULL,
alum_year_batch VARCHAR(20) NOT NULL,
alum_date_add DATE DEFAULT CURRENT_DATE ,
alum_year_grad INTEGER not null,
alum_delete_ind BOOLEAN DEFAULT FALSE NOT NULL,
appbatch_id integer,
degree_id INTEGER NOT NULL,
spec_id INTEGER,
CONSTRAINT appbatch_id_fkey FOREIGN KEY (appbatch_id) REFERENCES appbatch(appbatch_id),	
CONSTRAINT degree_id_fkey FOREIGN KEY (degree_id) REFERENCES degree(degree_id),
CONSTRAINT spec_id_fkey FOREIGN KEY (spec_id) REFERENCES specialization(spec_id)
);

INSERT INTO alumni (alum_fn,    alum_mn,    alum_ln,    alum_sf,    alum_st_num,    alum_cn,    alum_email, appbatch_id, alum_year_batch,   alum_date_add,  alum_year_grad, alum_delete_ind,    degree_id, spec_id)
VALUES
    ('James',   'Garcia',   'Hernandez',    null,   '197012345',    '09123456789',  'james.garcia@email.com',   7,  1976,   '2020-07-15',   1977,   FALSE,  1, 1),
    ('Emma',    'Santos',   'Gonzalez', null,   '198023456',    '09987654321',  'emma.santos@email.com',    7,  1980,   '2021-03-28',   1985,   FALSE,  2, 5),
    ('Alexander',   null,   'Lopez',    null,   '199034567',    '09456789012',  'alexander.lopez@email.com',    7,  1990,   '2022-10-10',   1996,   FALSE,  3, 2),
    ('Isabella',    'Cruz', 'Perez',    'III',  '200045678',    '09789012345',  'isabella.cruz@email.com',      7,   2000,   '2023-05-21',   2005,   FALSE,  4, 3),
    ('William', 'Reyes',    'Martinez', null,   '201056789',    '09234567890',  'william.reyes@email.com',  7,  2010,   '2024-12-03',   2015,   FALSE,  5, 4);

CREATE TABLE performance(
    perf_id SERIAL PRIMARY KEY not null,
    perf_acad_year varchar(50) not null,
    perf_reaff_comm1 integer,
    perf_comm1_score integer,
    perf_reaff_comm2 integer,
    perf_comm2_score integer,
    perf_eval NUMERIC,
    perf_delete_ind bool default false not null,
	mem_id integer,
CONSTRAINT perf_mem_id_fkey FOREIGN KEY (mem_id) REFERENCES member(mem_id),
CONSTRAINT perf_reaff_comm1_fkey FOREIGN KEY (perf_reaff_comm1) REFERENCES reaffiliation(reaff_id),
CONSTRAINT perf_reaff_comm2_fkey FOREIGN KEY (perf_reaff_comm2) REFERENCES reaffiliation(reaff_id)
);

INSERT INTO performance (mem_id, perf_acad_year, perf_reaff_comm1, perf_comm1_score, perf_reaff_comm2, perf_comm2_score, perf_eval, perf_delete_ind)
VALUES
(1,'2022-2023', 1, 88, 6, 98, 93, FALSE),
(2,'2019-2020', 2, 96, 7, 78, 87, FALSE),
(3,'2020-2021', 3, 75, 8, 60, 67.5, FALSE),
(4,'2023-2024', 4, 90, 9, 85, 87.5, FALSE),
(5,'2018-2019', 5, 87, 10, 99, 93, FALSE);

select
	perf_acad_year,
	c1.comm_name as FirstSem,
	perf_comm1_score as FirstSemScore,
	c2.comm_name as SecondSem,
	perf_comm2_score as SecondSemScore,
	perf_eval
from performance p
join reaffiliation r1 on r1.reaff_id = p.perf_reaff_comm1
join committee c1 on c1.comm_id = r1.reaff_assigned_comm
join reaffiliation r2 on r2.reaff_id = p.perf_reaff_comm2
join committee c2 on c2.comm_id = r2.reaff_assigned_comm;


-- Academic year 2019-2020
INSERT INTO member (mem_fn, mem_mn, mem_ln, mem_sf, mem_st_num, mem_bd, mem_cn, mem_emergency, mem_email, mem_up_email, mem_pres_add, mem_perma_add, mem_year_batch, appbatch_id, mem_year_standing, degree_id, mem_other_org, status_id, memtype_id, mem_reaffiliated, mem_is_new, mem_delete_ind)
VALUES
('Alice', 'Marie', 'Taylor', null, '201900456', '1995-02-20', '09123456789', '09876543210', 'alice.taylor@example.com', 'alice.marie@up.edu.ph', '123 Main St., Quezon City, Metro Manila', 'Block 5, Lot 10, Phase 2, Ayala Alabang, Muntinlupa City', 2018, 4, 2, 2, 'UP ACME', 1, 2, FALSE, TRUE, FALSE),
('Brandon', 'Lee', 'Martinez', null, '201901234', '1996-05-10', '09876543210', '09123456789', 'brandon.martinez@example.com', 'brandon.lee@up.edu.ph', '456 Elm St., Makati City, Metro Manila', 'Unit 301, Tower 2, Rockwell Center, Makati City', 2017, 4, 4, 3, 'IE Club', 1, 1, TRUE, FALSE, FALSE),
('Charlotte', 'Ann', 'Lopez', null, '201902345', '1997-08-15', '09456789012', '09765432109', 'charlotte.lopez@example.com', 'charlotte.ann@up.edu.ph', '789 Oak St., Taguig City, Metro Manila', 'Block 10, Lot 15, Phase 3, Greenheights Subd., Paranaque City', 2016, 4, 5, 1, 'ECE Society', 2, 3, TRUE, TRUE, FALSE);

-- Academic year 2020-2021
INSERT INTO member (mem_fn, mem_mn, mem_ln, mem_sf, mem_st_num, mem_bd, mem_cn, mem_emergency, mem_email, mem_up_email, mem_pres_add, mem_perma_add, mem_year_batch, appbatch_id, mem_year_standing, degree_id, mem_other_org, status_id, memtype_id, mem_reaffiliated, mem_is_new, mem_delete_ind)
VALUES
('David', 'Andrew', 'White', null, '202300001', '1998-03-25', '09234567890', '09543210987', 'david.white@example.com', 'david.andrew@up.edu.ph', 'Unit 101, Acacia Residences, Makati City, Metro Manila', 'Block 7, Lot 12, Phase 3, Villa Caceres Subdivision, Bacolod City, Negros Occidental', 2017, 4, 3, 1, 'UP CIEM', 1, 3, TRUE, TRUE, FALSE),
('Emma', 'Sophia', 'Brown', null, '202301234', '1999-06-15', '09123456789', '09876543210', 'emma.brown@example.com', 'emma.sophia@up.edu.ph', 'Block 3, Lot 5, Phase 2, BF Homes, Parañaque City, Metro Manila', 'Unit 301, Tower 1, Acacia Estates, Taguig City, Metro Manila', 2018, 3, 1, 2, 'IEC', 2, 4, FALSE, FALSE, FALSE),
('Felix', 'James', 'Clark', 'III', '202302345', '2000-09-10', '09765432109', '09456789012', 'felix.clark@example.com', 'felix.james@up.edu.ph', 'Purok 2, Brgy. Poblacion, Davao City, Davao del Sur', 'Phase 2, Block 5, Lot 8, Villa de Mercedes, Davao City, Davao del Sur', 2019, 3, 5, 3, 'N/A', 1, 1, TRUE, TRUE, FALSE);

-- Academic year 2021-2022
INSERT INTO member (mem_fn, mem_mn, mem_ln, mem_sf, mem_st_num, mem_bd, mem_cn, mem_emergency, mem_email, mem_up_email, mem_pres_add, mem_perma_add, mem_year_batch, appbatch_id, mem_year_standing, degree_id, mem_other_org, status_id, memtype_id, mem_reaffiliated, mem_is_new, mem_delete_ind)
VALUES
('Grace', 'Michelle', 'Harris', null, '202400345', '2001-03-20', '09345678901', '09871234567', 'grace.harris@example.com', 'grace.michelle@up.edu.ph', 'Lot 15, Phase 1, Northcrest Subdivision, Bacolod City, Negros Occidental', 'Blk 10, Lot 15, Kingsville Hills Subdivision, Antipolo City, Rizal', 2020, 3, 2, 1, 'GEOP', 2, 2, FALSE, FALSE, FALSE),
('Hannah', 'Elizabeth', 'Lee', null, '202401678', '2002-08-30', '09456789012', '09234567890', 'hannah.lee@example.com', 'hannah.elizabeth@up.edu.ph', 'Purok 4, Brgy. Masagana, Quezon City, Metro Manila', 'Blk 20, Lot 30, Phase 2, Greenview Subdivision, Marikina City', 2021, 3, 3, 2, 'IEC, CSA', 1, 3, TRUE, TRUE, FALSE),
('Isaac', 'William', 'Martinez', null, '202500001', '2003-02-15', '09567890123', '09123456789', 'isaac.martinez@example.com', 'isaac.william@up.edu.ph', 'Unit 201, Acacia Residences, Makati City, Metro Manila', 'Block 8, Lot 15, Phase 4, Villa Caceres Subdivision, Bacolod City, Negros Occidental', 2018, 3, 2, 2, 'UP ACME', 1, 2, FALSE, TRUE, FALSE);

-- Academic year 2019-2020
INSERT INTO reaffiliation (reaff_is_new, reaff_date, reaff_sem, reaff_acad_year, reaff_choice1, reaff_choice2, reaff_choice3, reaff_choice4, reaff_choice5, reaff_choice6, reaff_is_paid, reaff_date_paid, reaff_delete_ind, mem_id, reaff_gwa, reaff_assigned_comm)
VALUES
(TRUE, '2020-01-01', '1st', '2019-2020', 4, 5, 2, 6, 3, 1, TRUE, '2020-01-01', FALSE, 6, 1.85, 1),
(FALSE, '2021-06-15', '2nd', '2019-2020', 3, 6, 2, 5, 1, 4, FALSE, '2021-07-15', FALSE, 7, 2.75, 2),
(TRUE, '2022-09-30', '2nd', '2019-2020', 6, 5, 1, 4, 3, 2, FALSE, '2022-10-30', FALSE, 8, 2.45, 3);

-- Academic year 2020-2021
INSERT INTO reaffiliation (reaff_is_new, reaff_date, reaff_sem, reaff_acad_year, reaff_choice1, reaff_choice2, reaff_choice3, reaff_choice4, reaff_choice5, reaff_choice6, reaff_is_paid, reaff_date_paid, reaff_delete_ind, mem_id, reaff_gwa, reaff_assigned_comm)
VALUES
(TRUE, '2020-01-01', '1st', '2020-2021', 4, 5, 2, 6, 3, 1, TRUE, '2020-01-01', FALSE, 9, 1.95, 1),
(FALSE, '2021-06-15', '2nd', '2020-2021', 3, 6, 2, 5, 1, 4, FALSE, '2021-07-15', FALSE, 10, 2.75, 2),
(TRUE, '2022-09-30', '2nd', '2020-2021', 6, 5, 1, 4, 3, 2, FALSE, '2022-10-30', FALSE, 11, 2.30, 3);

-- Academic year 2021-2022
INSERT INTO reaffiliation (reaff_is_new, reaff_date, reaff_sem, reaff_acad_year, reaff_choice1, reaff_choice2, reaff_choice3, reaff_choice4, reaff_choice5, reaff_choice6, reaff_is_paid, reaff_date_paid, reaff_delete_ind, mem_id, reaff_gwa, reaff_assigned_comm)
VALUES
(TRUE, '2020-01-01', '1st', '2021-2022', 4, 5, 2, 6, 3, 1, TRUE, '2020-01-01', FALSE, 12, 2.15, 1),
(FALSE, '2021-06-15', '2nd', '2021-2022', 3, 6, 2, 5, 1, 4, FALSE, '2021-07-15', FALSE, 13, 2.00, 2),
(TRUE, '2022-09-30', '2nd', '2021-2022', 6, 5, 1, 4, 3, 2, FALSE, '2022-10-30', FALSE, 14, 1.85, 3);

-- Academic year 2019-2020
INSERT INTO headship_score (mem_id, head_id, headscore_description, headscore_acad_year, headscore_score, headscore_delete_ind)
VALUES
(6, 1, 'Director for Academic Welfare', '2019-2020', 10, FALSE),
(6, 2, 'Committee Chair', '2019-2020', 8, FALSE),
(7, 3, 'EPM Ishikawa', '2019-2020', 5, FALSE),
(7, 4, 'Events Coordinator', '2019-2020', 2, FALSE),
(8, 3, 'Programs Manager Ishikawa', '2019-2020', 5, FALSE);

-- Academic year 2020-2021
INSERT INTO headship_score (mem_id, head_id, headscore_description, headscore_acad_year, headscore_score, headscore_delete_ind)
VALUES
(9, 1, 'Director for Academic Welfare', '2020-2021', 10, FALSE),
(9, 2, 'Committee Chair', '2020-2021', 8, FALSE),
(10, 3, 'EPM Ishikawa', '2020-2021', 8, FALSE),
(10, 4, 'Events Coordinator', '2020-2021', 2, FALSE),
(11, 1, 'Programs Manager Ishikawa', '2020-2021', 5, FALSE);

-- Academic year 2021-2022
INSERT INTO headship_score (mem_id, head_id, headscore_description, headscore_acad_year, headscore_score, headscore_delete_ind)
VALUES
(12, 1, 'Director for Academic Welfare', '2021-2022', 10, FALSE),
(12, 2, 'Committee Chair', '2021-2022', 10, FALSE),
(13, 3, 'EPM Ishikawa', '2021-2022', 8, FALSE),
(13, 4, 'Events Coordinator', '2021-2022', 2, FALSE),
(14, 3, 'Programs Manager Ishikawa', '2021-2022', 5, FALSE),
(14, 4, 'Anniversary Gathering Team Member', '2021-2022', 2, FALSE);

-- Academic year 2019-2020
INSERT INTO performance (perf_acad_year, perf_reaff_comm1, perf_comm1_score, perf_reaff_comm2, perf_comm2_score, perf_eval, perf_delete_ind, mem_id)
VALUES
('2019-2020', 11, 88, null, null, 44, FALSE, 6),
('2019-2020', null, null, 12, 78, 39, FALSE, 7),
('2019-2020', null, null, 13, 60, 30, FALSE, 8);

-- Academic year 2020-2021
INSERT INTO performance (perf_acad_year, perf_reaff_comm1, perf_comm1_score, perf_reaff_comm2, perf_comm2_score, perf_eval, perf_delete_ind, mem_id)
VALUES
('2020-2021', 14, 90, null, null, 45, FALSE, 9),
('2020-2021', null, null, 15, 60, 30, FALSE, 10),
('2020-2021', null, null, 16, 88, 44, FALSE, 11);

-- Academic year 2021-2022
INSERT INTO performance (perf_acad_year, perf_reaff_comm1, perf_comm1_score, perf_reaff_comm2, perf_comm2_score, perf_eval, perf_delete_ind, mem_id)
VALUES
('2021-2022', 17, 85, null, null, 47.5, FALSE, 12),
('2021-2022', null, null, 18, 78, 39, FALSE, 13),
('2021-2022', null, null, 19, 85, 47.5, FALSE, 14);

--newer
-- 2019-2020
INSERT INTO member (mem_fn, mem_mn, mem_ln, mem_sf, mem_st_num, mem_bd, mem_cn, mem_emergency, mem_email, mem_up_email, mem_pres_add, mem_perma_add, mem_year_batch, appbatch_id, mem_year_standing, degree_id, mem_other_org, status_id, memtype_id, mem_reaffiliated, mem_is_new, mem_delete_ind)
VALUES
('Daniel', 'Evan', 'Thompson', null, '201900678', '1995-02-20', '09123456789', '09876543210', 'daniel.thompson@example.com', 'daniel.evan@up.edu.ph', '123 Main St., Quezon City, Metro Manila', 'Block 5, Lot 10, Phase 2, Ayala Alabang, Muntinlupa City', 2018, 4, 2, 2, 'UP ACME', 1, 2, FALSE, TRUE, FALSE),
('Sophia', 'Lynn', 'Garcia', null, '201901345', '1996-05-10', '09876543210', '09123456789', 'sophia.garcia@example.com', 'sophia.lynn@up.edu.ph', '456 Elm St., Makati City, Metro Manila', 'Unit 301, Tower 2, Rockwell Center, Makati City', 2017, 4, 4, 3, 'IE Club', 1, 1, TRUE, FALSE, FALSE),
('Jacob', 'Isaiah', 'Martinez', null, '201902678', '1997-08-15', '09456789012', '09765432109', 'jacob.martinez@example.com', 'jacob.isaiah@up.edu.ph', '789 Oak St., Taguig City, Metro Manila', 'Block 10, Lot 15, Phase 3, Greenheights Subd., Paranaque City', 2016, 4, 5, 1, 'ECE Society', 2, 3, TRUE, TRUE, FALSE),
('Liam', 'Noah', 'Sanchez', null, '201903789', '1997-04-25', '09123456789', '09876543210', 'liam.sanchez@example.com', 'liam.noah@up.edu.ph', '123 Maple St., Pasig City, Metro Manila', 'Block 8, Lot 5, Phase 1, Filinvest, Alabang', 2017, 4, 3, 2, 'UP Beta Epsilon', 1, 2, TRUE, TRUE, FALSE),
('Emma', 'Grace', 'Rodriguez', null, '201904567', '1996-11-20', '09123456789', '09876543210', 'emma.rodriguez@example.com', 'emma.grace@up.edu.ph', '789 Birch St., Quezon City, Metro Manila', 'Block 7, Lot 10, Phase 3, BF Homes, Parañaque City', 2016, 4, 4, 1, 'UP CIEM', 2, 1, FALSE, TRUE, FALSE);

--2020-2021

INSERT INTO member (mem_fn, mem_mn, mem_ln, mem_sf, mem_st_num, mem_bd, mem_cn, mem_emergency, mem_email, mem_up_email, mem_pres_add, mem_perma_add, mem_year_batch, appbatch_id, mem_year_standing, degree_id, mem_other_org, status_id, memtype_id, mem_reaffiliated, mem_is_new, mem_delete_ind)
VALUES
('Mason', 'Noah', 'Lopez', null, '202300567', '1998-03-25', '09234567890', '09543210987', 'mason.lopez@example.com', 'mason.noah@up.edu.ph', 'Unit 101, Acacia Residences, Makati City, Metro Manila', 'Block 7, Lot 12, Phase 3, Villa Caceres Subdivision, Bacolod City, Negros Occidental', 2017, 4, 3, 1, 'UP CIEM', 1, 3, TRUE, TRUE, FALSE),
('Isabella', 'Rose', 'Hernandez', null, '202301678', '1999-06-15', '09123456789', '09876543210', 'isabella.hernandez@example.com', 'isabella.rose@up.edu.ph', 'Block 3, Lot 5, Phase 2, BF Homes, Parañaque City, Metro Manila', 'Unit 301, Tower 1, Acacia Estates, Taguig City, Metro Manila', 2018, 3, 1, 2, 'IEC', 2, 4, FALSE, FALSE, FALSE),
('Logan', 'James', 'Clark', 'IV', '202302678', '2000-09-10', '09765432109', '09456789012', 'logan.clark@example.com', 'logan.james@up.edu.ph', 'Purok 2, Brgy. Poblacion, Davao City, Davao del Sur', 'Phase 2, Block 5, Lot 8, Villa de Mercedes, Davao City, Davao del Sur', 2019, 3, 5, 3, 'N/A', 1, 1, TRUE, TRUE, FALSE),
('Olivia', 'Mae', 'Johnson', null, '202303456', '1998-07-25', '09123456789', '09876543210', 'olivia.johnson@example.com', 'olivia.mae@up.edu.ph', '456 Pine St., Makati City, Metro Manila', 'Unit 202, Tower 3, Rockwell Center, Makati City', 2018, 4, 4, 3, 'IE Club', 2, 1, FALSE, TRUE, FALSE),
('Lucas', 'Michael', 'Brown', null, '202304567', '1999-11-20', '09123456789', '09876543210', 'lucas.brown@example.com', 'lucas.michael@up.edu.ph', '789 Cedar St., Taguig City, Metro Manila', 'Block 8, Lot 5, Phase 1, Filinvest, Alabang', 2017, 4, 5, 1, 'ECE Society', 1, 2, TRUE, TRUE, FALSE);

-- 2021-2022

INSERT INTO member (mem_fn, mem_mn, mem_ln, mem_sf, mem_st_num, mem_bd, mem_cn, mem_emergency, mem_email, mem_up_email, mem_pres_add, mem_perma_add, mem_year_batch, appbatch_id, mem_year_standing, degree_id, mem_other_org, status_id, memtype_id, mem_reaffiliated, mem_is_new, mem_delete_ind)
VALUES
('Grace', 'Michelle', 'Harris', null, '202400678', '2001-03-20', '09345678901', '09871234567', 'grace.harris@example.com', 'grace.michelle@up.edu.ph', 'Lot 15, Phase 1, Northcrest Subdivision, Bacolod City, Negros Occidental', 'Blk 10, Lot 15, Kingsville Hills Subdivision, Antipolo City, Rizal', 2020, 3, 2, 1, 'GEOP', 2, 2, FALSE, FALSE, FALSE),
('Hannah', 'Elizabeth', 'Lee', null, '202401678', '2002-08-30', '09456789012', '09234567890', 'hannah.lee@example.com', 'hannah.elizabeth@up.edu.ph', 'Purok 4, Brgy. Masagana, Quezon City, Metro Manila', 'Blk 20, Lot 30, Phase 2, Greenview Subdivision, Marikina City', 2021, 3, 3, 2, 'IEC, CSA', 1, 3, TRUE, TRUE, FALSE),
('Isaac', 'William', 'Martinez', null, '202500001', '2003-02-15', '09567890123', '09123456789', 'isaac.martinez@example.com', 'isaac.william@up.edu.ph', 'Unit 201, Acacia Residences, Makati City, Metro Manila', 'Block 8, Lot 15, Phase 4, Villa Caceres Subdivision, Bacolod City, Negros Occidental', 2018, 3, 2, 2, 'UP ACME', 1, 2, FALSE, TRUE, FALSE),
('Ella', 'Marie', 'Walker', null, '202402789', '2001-05-05', '09345678901', '09871234567', 'ella.walker@example.com', 'ella.marie@up.edu.ph', '123 Oak St., Quezon City, Metro Manila', 'Blk 15, Lot 20, Phase 3, Greenhills Subd., San Juan City', 2019, 4, 2, 1, 'UP Circuit', 2, 1, TRUE, TRUE, FALSE),
('Caleb', 'John', 'White', null, '202403890', '2002-07-25', '09345678901', '09871234567', 'caleb.white@example.com', 'caleb.john@up.edu.ph', '456 Birch St., Pasig City, Metro Manila', 'Blk 8, Lot 5, Phase 2, Filinvest, Alabang', 2020, 4, 4, 3, 'UP Circuit', 1, 3, TRUE, TRUE, FALSE);

-- Academic Year 2019-2020
INSERT INTO reaffiliation (reaff_is_new, reaff_date, reaff_sem, reaff_acad_year, reaff_choice1, reaff_choice2, reaff_choice3, reaff_choice4, reaff_choice5, reaff_choice6, reaff_is_paid, reaff_date_paid, reaff_delete_ind, mem_id, reaff_gwa, reaff_assigned_comm)
VALUES
(TRUE, '2019-08-01', '1st', '2019-2020', 1, 2, 4, 3, 5, 6, TRUE, '2019-08-10', FALSE, (SELECT mem_id FROM member WHERE mem_fn='Daniel' AND mem_ln='Thompson'), 2.15, 1),
(TRUE, '2020-01-15', '2nd', '2019-2020', 1, 2, 3, 4, 6, 3, TRUE, '2020-01-20', FALSE, (SELECT mem_id FROM member WHERE mem_fn='Daniel' AND mem_ln='Thompson'), 1.15, 2),

(TRUE, '2019-08-01', '1st', '2019-2020', 1, 3, 4, 2, 5, 6, TRUE, '2019-08-10', FALSE, (SELECT mem_id FROM member WHERE mem_fn='Sophia' AND mem_ln='Garcia'), 2.75, 3),
(TRUE, '2020-01-15', '2nd', '2019-2020', 6, 2, 3, 4, 5, 1, TRUE, '2020-01-20', FALSE, (SELECT mem_id FROM member WHERE mem_fn='Sophia' AND mem_ln='Garcia'), 2.25, 6),

(TRUE, '2019-08-01', '1st', '2019-2020', 1, 6, 3, 4, 5, 2, TRUE, '2019-08-10', FALSE, (SELECT mem_id FROM member WHERE mem_fn='Jacob' AND mem_ln='Martinez'), 1.35, 4),
(TRUE, '2020-01-15', '2nd', '2019-2020', 1, 4, 3, 5, 2, 6, TRUE, '2020-01-20', FALSE, (SELECT mem_id FROM member WHERE mem_fn='Jacob' AND mem_ln='Martinez'), 1.45, 3),

(TRUE, '2019-08-01', '1st', '2019-2020', 6, 5, 3, 4, 1, 2, TRUE, '2019-08-10', FALSE, (SELECT mem_id FROM member WHERE mem_fn='Liam' AND mem_ln='Sanchez'), 1.259, 3),
(TRUE, '2020-01-15', '2nd', '2019-2020', 3, 2, 1, 6, 5, 4, TRUE, '2020-01-20', FALSE, (SELECT mem_id FROM member WHERE mem_fn='Liam' AND mem_ln='Sanchez'), 1.234, 5),
(TRUE, '2019-08-01', '1st', '2019-2020', 4, 3, 3, 1, 5, 6, TRUE, '2019-08-10', FALSE, (SELECT mem_id FROM member WHERE mem_fn='Emma' AND mem_ln='Rodriguez'), 1.2345, 2),
(TRUE, '2020-01-15', '2nd', '2019-2020', 2, 1, 4, 3, 6, 5, TRUE, '2020-01-20', FALSE, (SELECT mem_id FROM member WHERE mem_fn='Emma' AND mem_ln='Rodriguez'), 2.2222, 2);

-- Academic Year 2020-2021
INSERT INTO reaffiliation (reaff_is_new, reaff_date, reaff_sem, reaff_acad_year, reaff_choice1, reaff_choice2, reaff_choice3, reaff_choice4, reaff_choice5, reaff_choice6, reaff_is_paid, reaff_date_paid, reaff_delete_ind, mem_id, reaff_gwa, reaff_assigned_comm)
VALUES
(TRUE, '2020-08-01', '1st', '2020-2021', 3, 4, 2, 1, 6, 5, TRUE, '2020-08-10', FALSE, (SELECT mem_id FROM member WHERE mem_fn='Mason' AND mem_ln='Lopez'), 2.45, 1),
(TRUE, '2021-01-15', '2nd', '2020-2021', 5, 1, 3, 2, 6, 4, TRUE, '2021-01-20', FALSE, (SELECT mem_id FROM member WHERE mem_fn='Mason' AND mem_ln='Lopez'), 1.45, 2),

(TRUE, '2020-08-01', '1st', '2020-2021', 4, 2, 5, 3, 1, 6, TRUE, '2020-08-10', FALSE, (SELECT mem_id FROM member WHERE mem_fn='Isabella' AND mem_ln='Hernandez'), 2.55, 3),
(TRUE, '2021-01-15', '2nd', '2020-2021', 2, 6, 1, 3, 5, 4, TRUE, '2021-01-20', FALSE, (SELECT mem_id FROM member WHERE mem_fn='Isabella' AND mem_ln='Hernandez'), 1.55, 4),

(TRUE, '2020-08-01', '1st', '2020-2021', 6, 3, 1, 5, 2, 4, TRUE, '2020-08-10', FALSE, (SELECT mem_id FROM member WHERE mem_fn='Logan' AND mem_ln='Clark'), 2.05, 5),
(TRUE, '2021-01-15', '2nd', '2020-2021', 4, 1, 6, 2, 3, 5, TRUE, '2021-01-20', FALSE, (SELECT mem_id FROM member WHERE mem_fn='Logan' AND mem_ln='Clark'), 2.35, 6),

(TRUE, '2020-08-01', '1st', '2020-2021', 2, 1, 3, 6, 4, 5, TRUE, '2020-08-10', FALSE, (SELECT mem_id FROM member WHERE mem_fn='Olivia' AND mem_ln='Johnson'), 1.25, 3),
(TRUE, '2021-01-15', '2nd', '2020-2021', 3, 5, 2, 1, 6, 4, TRUE, '2021-01-20', FALSE, (SELECT mem_id FROM member WHERE mem_fn='Olivia' AND mem_ln='Johnson'), 1.75, 2),

(TRUE, '2020-08-01', '1st', '2020-2021', 5, 4, 2, 6, 3, 1, TRUE, '2020-08-10', FALSE, (SELECT mem_id FROM member WHERE mem_fn='Lucas' AND mem_ln='Brown'), 1.75, 1),
(TRUE, '2021-01-15', '2nd', '2020-2021', 1, 3, 4, 5, 2, 6, TRUE, '2021-01-20', FALSE, (SELECT mem_id FROM member WHERE mem_fn='Lucas' AND mem_ln='Brown'), 1.85, 4);

-- Academic Year 2021-2022
INSERT INTO reaffiliation (reaff_is_new, reaff_date, reaff_sem, reaff_acad_year, reaff_choice1, reaff_choice2, reaff_choice3, reaff_choice4, reaff_choice5, reaff_choice6, reaff_is_paid, reaff_date_paid, reaff_delete_ind, mem_id, reaff_gwa, reaff_assigned_comm)
VALUES
(TRUE, '2021-08-01', '1st', '2021-2022', 4, 1, 6, 3, 2, 5, TRUE, '2021-08-10', FALSE, 25, 2.25, 2),
(TRUE, '2022-01-15', '2nd', '2021-2022', 6, 2, 4, 1, 5, 3, TRUE, '2022-01-20', FALSE, 25, 1.95, 2),

(TRUE, '2021-08-01', '1st', '2021-2022', 2, 4, 1, 3, 6, 5, TRUE, '2021-08-10', FALSE, 26, 1.05, 1),
(TRUE, '2022-01-15', '2nd', '2021-2022', 5, 3, 6, 1, 4, 2, TRUE, '2022-01-20', FALSE, 26, 1.34, 1),

(TRUE, '2021-08-01', '1st', '2021-2022', 3, 5, 1, 6, 2, 4, TRUE, '2021-08-10', FALSE, 27, 1.15, 4),
(TRUE, '2022-01-15', '2nd', '2021-2022', 4, 1, 5, 2, 6, 3, TRUE, '2022-01-20', FALSE, 27, 2.15, 4),

(TRUE, '2021-08-01', '1st', '2021-2022', 1, 3, 6, 4, 5, 2, TRUE, '2021-08-10', FALSE, 28, 1.025, 5),
(TRUE, '2022-01-15', '2nd', '2021-2022', 3, 5, 1, 6, 4, 2, TRUE, '2022-01-20', FALSE, 28, 1.0000, 6),

(TRUE, '2021-08-01', '1st', '2021-2022', 5, 2, 1, 3, 6, 4, TRUE, '2021-08-10', FALSE, 29, 1.322, 3),
(TRUE, '2022-01-15', '2nd', '2021-2022', 2, 4, 3, 5, 1, 6, TRUE, '2022-01-20', FALSE, 29, 1.35, 3);

-- Headship Scores for Academic Year 2019-2020
INSERT INTO headship_score (mem_id, head_id, headscore_description, headscore_acad_year, headscore_score, headscore_delete_ind)
VALUES
(15, 1, 'Director for Academic Welfare', '2019-2020', 10, FALSE),
(15, 2, 'Committee Chair', '2019-2020', 8, FALSE),
(16, 3, 'EPM Ishikawa', '2019-2020', 5, FALSE),
(16, 4, 'Events Coordinator', '2019-2020', 2, FALSE),
(17, 3, 'Programs Manager Ishikawa', '2019-2020', 5, FALSE),
(17, 1, 'Director for Academic Welfare', '2019-2020', 10, FALSE),
(18, 2, 'Committee Chair', '2019-2020', 8, FALSE),
(18, 3, 'EPM Ishikawa', '2019-2020', 5, FALSE),
(19, 4, 'Events Coordinator', '2019-2020', 2, FALSE),
(19, 3, 'Programs Manager Ishikawa', '2019-2020', 5, FALSE);

-- Headship Scores for Academic Year 2020-2021
INSERT INTO headship_score (mem_id, head_id, headscore_description, headscore_acad_year, headscore_score, headscore_delete_ind)
VALUES
(20, 1, 'Director for Academic Welfare', '2020-2021', 10, FALSE),
(20, 2, 'Committee Chair', '2020-2021', 8, FALSE),
(21, 3, 'EPM Ishikawa', '2020-2021', 5, FALSE),
(21, 4, 'Events Coordinator', '2020-2021', 2, FALSE),
(22, 3, 'Programs Manager Ishikawa', '2020-2021', 5, FALSE),
(22, 1, 'Director for Academic Welfare', '2020-2021', 10, FALSE),
(23, 2, 'Committee Chair', '2020-2021', 8, FALSE),
(23, 3, 'EPM Ishikawa', '2020-2021', 5, FALSE),
(24, 4, 'Events Coordinator', '2020-2021', 2, FALSE),
(24, 3, 'Programs Manager Ishikawa', '2020-2021', 5, FALSE);

-- Headship Scores for Academic Year 2021-2022
INSERT INTO headship_score (mem_id, head_id, headscore_description, headscore_acad_year, headscore_score, headscore_delete_ind)
VALUES
(25, 1, 'Director for Academic Welfare', '2021-2022', 10, FALSE),
(25, 2, 'Committee Chair', '2021-2022', 8, FALSE),
(26, 3, 'EPM Ishikawa', '2021-2022', 5, FALSE),
(26, 4, 'Events Coordinator', '2021-2022', 2, FALSE),
(27, 3, 'Programs Manager Ishikawa', '2021-2022', 5, FALSE),
(27, 1, 'Director for Academic Welfare', '2021-2022', 10, FALSE),
(28, 2, 'Committee Chair', '2021-2022', 8, FALSE),
(28, 3, 'EPM Ishikawa', '2021-2022', 5, FALSE),
(29, 4, 'Events Coordinator', '2021-2022', 2, FALSE),
(29, 3, 'Programs Manager Ishikawa', '2021-2022', 5, FALSE);

-- Performance Inserts for Academic Year 2019-2020
INSERT INTO performance (perf_acad_year, perf_reaff_comm1, perf_comm1_score, perf_reaff_comm2, perf_comm2_score, perf_eval, perf_delete_ind, mem_id)
VALUES
('2019-2020', 20, 88, 21, 44, 66, FALSE, 15),
('2019-2020', 22, 78, 23, 60, 69, FALSE, 16),
('2019-2020', 24, 90, 25, 85, 87.5, FALSE, 17),
('2019-2020', 26, 82, 27, 78, 80, FALSE, 18),
('2019-2020', 28, 85, 29, 80, 82.5, FALSE, 19);

-- Performance Inserts for Academic Year 2020-2021
INSERT INTO performance (perf_acad_year, perf_reaff_comm1, perf_comm1_score, perf_reaff_comm2, perf_comm2_score, perf_eval, perf_delete_ind, mem_id)
VALUES
('2020-2021', 30, 75, 31, 70, 72.5, FALSE, 20),
('2020-2021', 32, 78, 33, 82, 80, FALSE, 21),
('2020-2021', 34, 80, 35, 76, 78, FALSE, 22),
('2020-2021', 36, 82, 37, 78, 80, FALSE, 23),
('2020-2021', 38, 72, 39, 75, 73.5, FALSE, 24);

-- Performance Inserts for Academic Year 2021-2022
INSERT INTO performance (perf_acad_year, perf_reaff_comm1, perf_comm1_score, perf_reaff_comm2, perf_comm2_score, perf_eval, perf_delete_ind, mem_id)
VALUES
('2021-2022', 40, 88, 41, 85, 86.5, FALSE, 25),
('2021-2022', 42, 90, 43, 80, 85, FALSE, 26),
('2021-2022', 44, 82, 45, 78, 80, FALSE, 27),
('2021-2022', 46, 85, 47, 80, 83.5, FALSE, 28),
('2021-2022', 48, 72, 49, 75, 73.5, FALSE, 29);
