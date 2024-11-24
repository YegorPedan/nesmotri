package database

import (
	"fmt"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
	"mospolytech_app/config"
	"sync"
)

var (
	once       sync.Once
	dbInstance *postgresDatabase
)

func NewPostgresDatabase(conf *config.Config) Database {
	once.Do(func() {
		dsn := fmt.Sprintf("host=%s port=%s user=%s password=%s dbname=%s sslmode=%s TimeZone=%s",
			conf.DB.Host,
			conf.DB.Port,
			conf.DB.User,
			conf.DB.Password,
			conf.DB.DBName,
			conf.DB.SSLMode,
			conf.DB.TimeZone)

		db, err := gorm.Open(postgres.Open(dsn))
		if err != nil {
			panic("failed to connect database")
		}

		dbInstance = &postgresDatabase{
			DB: db,
		}
	})

	return dbInstance
}
