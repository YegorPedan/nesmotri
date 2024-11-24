package database

import "gorm.io/gorm"

type Database interface {
	GetDB() *gorm.DB
}

// PostgresDatabase
type postgresDatabase struct {
	DB *gorm.DB
}

func (p *postgresDatabase) GetDB() *gorm.DB {
	return dbInstance.DB
}
