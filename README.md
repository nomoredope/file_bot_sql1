# file_bot_sql
 ##################################################
 УСТАНОВКА БОТА НА ВАШУ СИСТЕМУ
 ##################################################
--------------------------------------------------------------
 1. Установите необходимые библиотеки/api/фреймворки
 1) pip install elevate
 2) pip install bs4
 3) pip install PyMySQL
 4) pip install pyTelegramBotAPI
 5) pip install requests
--------------------------------------------------------------
 2. Создайте базу данных (MySQL)
 1) CREATE SCHEMA `new_schema` ;
 2) CREATE TABLE `new_schema`.`user_data` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `chat_id` VARCHAR(45) NOT NULL,
  `username` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`));
  
 3) CREATE TABLE `new_schema`.`regs` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `login` VARCHAR(45) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  `personal_code` VARCHAR(45) NULL,
  PRIMARY KEY (`id`));
-------------------------------------------------------------- 
 3. Создайте файл visitors.txt
--------------------------------------------------------------
Подготовка к установке бота завершена!
