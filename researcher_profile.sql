-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jul 08, 2025 at 09:21 PM
-- Server version: 11.4.5-MariaDB-log
-- PHP Version: 8.3.22

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `crajendranadmk_researcher_profile`
--

-- --------------------------------------------------------

--
-- Table structure for table `color_settings`
--

CREATE TABLE `color_settings` (
  `id` int(11) NOT NULL,
  `header_color` varchar(7) DEFAULT NULL,
  `sidebar_color` varchar(7) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `color_settings`
--

INSERT INTO `color_settings` (`id`, `header_color`, `sidebar_color`) VALUES
(1, '#bfbfbf', '#bfbfbf');

-- --------------------------------------------------------

--
-- Table structure for table `details`
--

CREATE TABLE `details` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `institution` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone` varchar(50) NOT NULL,
  `address` text NOT NULL,
  `website` varchar(255) DEFAULT NULL,
  `profile_picture` varchar(255) DEFAULT NULL,
  `research_areas` text NOT NULL,
  `research_ids` text DEFAULT NULL,
  `education` text DEFAULT NULL,
  `funding` text DEFAULT NULL,
  `publications` text DEFAULT NULL,
  `career_highlights` text DEFAULT NULL,
  `research_career` text DEFAULT NULL,
  `department` varchar(255) DEFAULT NULL,
  `Title` varchar(255) DEFAULT NULL,
  `collab` text DEFAULT NULL,
  `visit_count` int(11) DEFAULT 0,
  `phd_scholars_produced` int(11) DEFAULT 0,
  `phd_scholars_registered` int(11) DEFAULT 0,
  `phd_scholars` text DEFAULT NULL,
  `alternative_email` varchar(255) DEFAULT NULL,
  `consultancy` text DEFAULT NULL,
  `administrative_position` text DEFAULT NULL,
  `honorary_positions` text DEFAULT NULL,
  `conferences` text DEFAULT NULL,
  `resource_person` text DEFAULT NULL,
  `department_order` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `details`
--

INSERT INTO `details` (`id`, `name`, `institution`, `email`, `phone`, `address`, `website`, `profile_picture`, `research_areas`, `research_ids`, `education`, `funding`, `publications`, `career_highlights`, `research_career`, `department`, `Title`, `collab`, `visit_count`, `phd_scholars_produced`, `phd_scholars_registered`, `phd_scholars`, `alternative_email`, `consultancy`, `administrative_position`, `honorary_positions`, `conferences`, `resource_person`, `department_order`) VALUES
(75, 'Mr Saran', 'Madras Christian College', 'saran@mcc.edu.in', '9499954810', '3/943 Mandaveli st ,Meavakam, Chennai 600 100', 'http://127.0.0.1:8000/', 'Saran_1731266349.png', 'Saran', '[{\"title\": \"Saran\", \"id\": \"http://127.0.0.1:8000/\"}]', '[]', '[{\"project_title\": \"Saran\", \"funding_agency\": \"Saran\", \"year\": \"December 2024\", \"amount\": \"100000\", \"status\": \"completed\"}]', '[{\"date\": \"January 2024\", \"type\": \"Book\", \"title\": \"Saran\", \"link\": \"https://doi.org/10.1039/D3NJ03762B\"}]', 'Saran', 'Saran', 'MCC - MRF Innovation Park', 'proefssor', 'Saran', 29, 1, 1, '[{\"name\": \"Saran\", \"topic\": \"Saran\", \"status\": \"completed\", \"years_of_completion\": \"2020\"}]', 'saran@mcc.edu.in', 'Saran', '[{\"position\": \"Saran\", \"year_from\": \"2020\", \"year_to\": \"2020\"}]', '[{\"position\": \"Saran\", \"year\": \"2020\"}]', '[{\"year\": \"December 2024\", \"type\": \"International\", \"title_of_paper\": \"Saran\", \"details\": \"Saran\", \"isbn\": \"Saran\"}]', '[{\"date\": \"January 2024\", \"topic\": \"Saran\", \"department_\": \"Saran\"}]', 10),
(82, 'Mr Dr.r Vijay Solomon', 'Madras Christian College', 'x@mcc.edu.in', '9841214393', '3/943 Mandaveli st ,Meavakam, Chennai 600 100', 'http://vjsolo.weebly.com/', 'DR.R_VIJAY_SOLOMON_1731671055.png', '', '[]', '[{\"degree\": \"xcv\", \"college\": \"cxv\", \"duration\": \"2345\"}]', '[{\"project_title\": \"sdf\", \"funding_agency\": \"breakoutzone\", \"year\": \"July 2024\", \"amount\": \"2000000\", \"status\": \"completed\"}, {\"project_title\": \"sdf\", \"funding_agency\": \"breakouzone\", \"year\": \"July 2024\", \"amount\": \"200000000\", \"status\": \"ongoing\"}]', '[]', '', '', 'MCC - MRF Innovation Park', 'dfgfd', '', 3, 0, 0, '[]', 'juli@gmail.com', '', '[]', '[]', '[{\"year\": \"December 2024\", \"type\": \"International\", \"title_of_paper\": \"Saran\", \"details\": \"Saran\", \"isbn\": \"324\"}, {\"year\": \"August 2024\", \"type\": \"National\", \"title_of_paper\": \"fgd\", \"details\": \"sa\", \"isbn\": \"14124\"}]', '[]', 2),
(83, 'Mr Sample 2', 'Madras Christian College', 'a@mcc.edu.in', '9841214393', '3/943', 'http://127.0.0.1:8000/', 'Sample_2_1733669668.png', '', '[]', '[]', '[]', '[]', '', '', 'MCC - MRF Innovation Park', 'porfessor', '', 1, 0, 0, '[]', 'juli@gmail.com', '', '[]', '[]', '[]', '[]', 20),
(84, 'Mr Sample 3', 'Madras Christian College', 'b@mcc.edu.in', '9841214393', '3/943 Mandaveli st ,Meavakam, Chennai 600 100', 'http://127.0.0.1:8000/', 'Sample_3_1733670290.png', '', '[]', '[]', '[]', '[]', '', '', 'MCC - MRF Innovation Park', 'poefssor', '', 0, 0, 0, '[]', 'm@mcc.edu.in', '', '[]', '[]', '[]', '[]', 5),
(85, 'Dr Saran T', 'Madras Christian College', 'c@mcc.edu.in', '9841214393', '3/943 Mandaveli st ,Meavakam, Chennai 600 100', 'http://127.0.0.1:8000/', 'Saran_T_1733755013.png', '', '[]', '[]', '[]', '[]', '', '', 'MCC - MRF Innovation Park', 'head od the department', '', 0, 0, 0, '[]', 'saran@mcc.edu.in', '', '[]', '[]', '[]', '[]', 10),
(86, 'Dr Saran T', 'Madras Christian College', 'd@mcc.edu.in', '9841214393', '3/943 mandaveli st ,meavakam', 'http://127.0.0.1:8000/', 'Saran_T_1733755111.png', '', '[]', '[]', '[]', '[]', '', '', 'MCC - MRF Innovation Park', 'Dean of Student Affairs', '', 0, 0, 0, '[]', 'saran@mcc.edu.in', '', '[]', '[]', '[]', '[]', 17),
(87, 'Mr Saran T ( Test User1)', 'Madras Christian College', 'e@mcc.edu.in', '9597618759', '3/943 Mandaveli st ,Meavakam, Chennai 600 100', 'http://127.0.0.1:5000/', 'Saran_T__Test_User1_1733755313.png', '', '[]', '[]', '[]', '[]', '', '', 'MCC - MRF Innovation Park', 'Assistant Professor', '', 0, 0, 0, '[]', 'saran@mcc.edu.in', '', '[]', '[]', '[]', '[]', 19),
(90, 'Dr Saran T ( Test User1)', 'Madras Christian College', 'f@mcc.edu.in', '9841214393', '3/943 Mandaveli st ,Meavakam, Chennai 600 100', 'http://127.0.0.1:8000/', 'Saran_T__Test_User1_1733757191.png', 'fds', '[{\"title\": \"sdsd\", \"id\": \"http://127.0.0.1:8000/s\"}]', '[{\"degree\": \"B.Sc.,Chemistry\", \"college\": \"St. Xavier\\u2019s College\", \"duration\": \"2020\"}]', '[{\"project_title\": \"A theoretical study on radical scavenging activity of phenolic derivatives naturally found within Alternaria alternata extract, Org. Biomol. Chem., 2024\", \"funding_agency\": \"breakoutzone\", \"year\": \"January 2024\", \"amount\": \"2000000\", \"status\": \"completed\"}]', '[{\"date\": \"July 2024\", \"type\": \"Conference paper\", \"title\": \"A theoretical study on radical scavenging activity of phenolic derivatives naturally found within Alternaria alternata extract, Org. Biomol. Chem., 2024\", \"link\": \"https://github.com/Saran1708/Resume/tree/main\"}, {\"date\": \"February 2024\", \"type\": \"newwww dummy\", \"title\": \"A theoretical study on radical scavenging activity of phenolic derivatives naturally found within Alternaria alternata extract, Org. Biomol. Chem., 2024\", \"link\": \"https://doi.org/10.1039/D3NJ03762B\"}, {\"date\": \"August 2024\", \"type\": \"newwww2\", \"title\": \"Computational Tools and Techniques in Designing Ligands for the Selective Separation of Actinide and Lanthanide: A Review , Comments in InOrg. Chem., 2024\", \"link\": \"http://127.0.0.1:8000/\"}]', 'dsfds', 'sdf', 'MCC - MRF Innovation Park', 'Associate Professor', 'xdfds', 1, NULL, NULL, '[]', 'saran17sakthi@gmail.com', 'dsf', '[{\"position\": \"placement cell represntative\", \"year_from\": \"2010\", \"year_to\": \"cureent\"}]', '[{\"position\": \"Kho kho Captain -  clg\", \"year\": \"2028\"}]', '[{\"year\": \"January 2024\", \"type\": \"International\", \"title_of_paper\": \"Saran\", \"details\": \"Option Conclave\", \"isbn\": \"17082003\"}]', '[{\"date\": \"January 2024\", \"topic\": \"sa\", \"department_\": \"BCA\"}]', 14);

-- --------------------------------------------------------

--
-- Table structure for table `staff`
--

CREATE TABLE `staff` (
  `id` int(11) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  `password_changed` tinyint(1) DEFAULT 0,
  `profile_completed` tinyint(1) DEFAULT 0,
  `role` varchar(50) NOT NULL DEFAULT 'staff'
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `staff`
--

INSERT INTO `staff` (`id`, `email`, `password`, `password_changed`, `profile_completed`, `role`) VALUES
(1, 'admin@mcc.edu.in', 'Mcc@321', 0, 0, 'admin'),
(2, 'admin2@mcc.edu.in', 'Mcc@321', 0, 0, 'admin'),
(89, 'saran@mcc.edu.in', '123456', 1, 1, 'staff'),
(96, 'x@mcc.edu.in', '123456', 1, 1, 'staff'),
(97, 'a@mcc.edu.in', '123456', 1, 1, 'staff'),
(98, 'b@mcc.edu.in', '123456', 1, 1, 'staff'),
(99, 'c@mcc.edu.in', '123456', 1, 1, 'staff'),
(100, 'd@mcc.edu.in', '123456', 1, 1, 'staff'),
(102, 'e@mcc.edu.in', '123456', 1, 1, 'staff'),
(105, 'f@mcc.edu.in', '123456', 1, 1, 'staff');

-- --------------------------------------------------------

--
-- Table structure for table `visit_logs`
--

CREATE TABLE `visit_logs` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `ip_address` varchar(45) NOT NULL,
  `timestamp` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `color_settings`
--
ALTER TABLE `color_settings`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `details`
--
ALTER TABLE `details`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `staff`
--
ALTER TABLE `staff`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `visit_logs`
--
ALTER TABLE `visit_logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `details`
--
ALTER TABLE `details`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=91;

--
-- AUTO_INCREMENT for table `staff`
--
ALTER TABLE `staff`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=106;

--
-- AUTO_INCREMENT for table `visit_logs`
--
ALTER TABLE `visit_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
