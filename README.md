﻿# file_bot_sql
 ##################################################
 УСТАНОВКА БОТА НА ВАШУ СИСТЕМУ
 ##################################################
--------------------------------------------------------------
 1. Установите необходимые библиотеки/api/фреймворки
 pip install elevate
 pip install bs4
 pip install PyMySQL
 pip install pyTelegramBotAPI
 pip install requests
--------------------------------------------------------------
 2. Создайте базу данных (MySQL)
 CREATE SCHEMA `new_schema` ;
 CREATE TABLE `new_schema`.`user_data` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `chat_id` VARCHAR(45) NOT NULL,
  `username` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`));
  
 CREATE TABLE `new_schema`.`regs` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `login` VARCHAR(45) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  `personal_code` VARCHAR(45) NULL,
  PRIMARY KEY (`id`));
-------------------------------------------------------------- 
 3. Создайте файл visitors.txt
--------------------------------------------------------------
Подготовка к установке бота завершена!
