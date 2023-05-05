-- MySQL Script generated by MySQL Workbench
-- Fri May  5 15:40:13 2023
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema prueba_dc1
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema prueba_dc1
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `prueba_dc1` DEFAULT CHARACTER SET utf8 ;
USE `prueba_dc1` ;

-- -----------------------------------------------------
-- Table `prueba_dc1`.`permiso`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `prueba_dc1`.`permiso` ;

CREATE TABLE IF NOT EXISTS `prueba_dc1`.`permiso` (
  `id_permiso` INT NOT NULL AUTO_INCREMENT,
  `nombre_permiso` VARCHAR(40) NULL,
  PRIMARY KEY (`id_permiso`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `prueba_dc1`.`rol`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `prueba_dc1`.`rol` ;

CREATE TABLE IF NOT EXISTS `prueba_dc1`.`rol` (
  `id_rol` INT NOT NULL AUTO_INCREMENT,
  `nombre_rol` VARCHAR(30) NOT NULL,
  `fk_id_permiso` INT NOT NULL,
  PRIMARY KEY (`id_rol`),
  INDEX `fk_rol_permiso1_idx` (`fk_id_permiso` ASC) ,
  CONSTRAINT `fk_rol_permiso1`
    FOREIGN KEY (`fk_id_permiso`)
    REFERENCES `prueba_dc1`.`permiso` (`id_permiso`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `prueba_dc1`.`comuna`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `prueba_dc1`.`comuna` ;

CREATE TABLE IF NOT EXISTS `prueba_dc1`.`comuna` (
  `id_comuna` INT NOT NULL AUTO_INCREMENT,
  `comuna` VARCHAR(45) NULL,
  PRIMARY KEY (`id_comuna`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `prueba_dc1`.`usuario`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `prueba_dc1`.`usuario` ;

CREATE TABLE IF NOT EXISTS `prueba_dc1`.`usuario` (
  `idusuario` INT NOT NULL AUTO_INCREMENT,
  `nombre_usuario` VARCHAR(50) NULL,
  `apellido_usuario` VARCHAR(50) NULL,
  `celular` INT NULL,
  `correo` VARCHAR(200) NULL,
  `direccion` VARCHAR(100) NULL,
  `fk_id_rol` INT NOT NULL,
  `fk_id_comuna` INT NOT NULL,
  PRIMARY KEY (`idusuario`),
  INDEX `fk_usuario_rol1_idx` (`fk_id_rol` ASC) ,
  INDEX `fk_usuario_comuna` (`fk_id_comuna` ASC) ,
  CONSTRAINT `fk_usuario_rol1`
    FOREIGN KEY (`fk_id_rol`)
    REFERENCES `prueba_dc1`.`rol` (`id_rol`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_usuario_comuna`
    FOREIGN KEY (`fk_id_comuna`)
    REFERENCES `prueba_dc1`.`comuna` (`id_comuna`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `prueba_dc1`.`proveedor`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `prueba_dc1`.`proveedor` ;

CREATE TABLE IF NOT EXISTS `prueba_dc1`.`proveedor` (
  `id_proveedor` INT NOT NULL,
  `nombre_proveedor` VARCHAR(100) NULL,
  `descripcion` VARCHAR(400) NULL,
  `rut_proveedor` VARCHAR(100) NULL,
  `direccion` VARCHAR(100) NULL,
  PRIMARY KEY (`id_proveedor`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `prueba_dc1`.`producto`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `prueba_dc1`.`producto` ;

CREATE TABLE IF NOT EXISTS `prueba_dc1`.`producto` (
  `idproducto` INT NOT NULL AUTO_INCREMENT,
  `nombre_producto` VARCHAR(100) NULL,
  `stock` INT NULL,
  `precio` INT NULL,
  `descripcion` VARCHAR(400) NULL,
  `fk_id_proveedor` INT NOT NULL,
  PRIMARY KEY (`idproducto`),
  INDEX `fk_producto_proveedor1_idx` (`fk_id_proveedor` ASC) ,
  CONSTRAINT `fk_producto_proveedor1`
    FOREIGN KEY (`fk_id_proveedor`)
    REFERENCES `prueba_dc1`.`proveedor` (`id_proveedor`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `prueba_dc1`.`carrito`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `prueba_dc1`.`carrito` ;

CREATE TABLE IF NOT EXISTS `prueba_dc1`.`carrito` (
  `idCarrito` INT NOT NULL AUTO_INCREMENT,
  `fk_id_producto` INT NOT NULL,
  `total` INT NULL,
  `fk_id_usuario` INT NOT NULL,
  PRIMARY KEY (`idCarrito`),
  INDEX `fk_Carrito_producto1_idx` (`fk_id_producto` ASC) ,
  INDEX `fk_Carrito_usuario1_idx` (`fk_id_usuario` ASC) ,
  CONSTRAINT `fk_Carrito_producto1`
    FOREIGN KEY (`fk_id_producto`)
    REFERENCES `prueba_dc1`.`producto` (`idproducto`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Carrito_usuario1`
    FOREIGN KEY (`fk_id_usuario`)
    REFERENCES `prueba_dc1`.`usuario` (`idusuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `prueba_dc1`.`pedido`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `prueba_dc1`.`pedido` ;

CREATE TABLE IF NOT EXISTS `prueba_dc1`.`pedido` (
  `id_pedido` INT NOT NULL,
  `descripcion` VARCHAR(400) NULL,
  `fecha` DATETIME NULL,
  `fk_id_producto` INT NOT NULL,
  PRIMARY KEY (`id_pedido`),
  INDEX `fk_pedido_producto_idx` (`fk_id_producto` ASC) ,
  CONSTRAINT `fk_pedido_producto`
    FOREIGN KEY (`fk_id_producto`)
    REFERENCES `prueba_dc1`.`producto` (`idproducto`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
