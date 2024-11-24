package main

import (
	"mospolytech_app/addiction/entities"
	"mospolytech_app/config"
	"mospolytech_app/database"
	"time"
)

func main() {
	conf := config.GetConfig()
	db := database.NewPostgresDatabase(conf)

	appMigrate(db)
}

func appMigrate(db database.Database) {
	err := db.GetDB().Migrator().CreateTable(&entities.Phone{})
	if err != nil {
		panic(err)
	}

	db.GetDB().CreateInBatches([]entities.Phone{
		{
			StudentName:       "Сизов Султан",
			PhoneModel:        "Samsung",
			PhoneCharge:       100,
			ConnectionTime:    time.Now(),
			DisconnectionTime: time.Now().Add(5 * time.Minute),
		},
		{
			StudentName:       "Славин Сергей",
			PhoneModel:        "Apple",
			PhoneCharge:       40,
			ConnectionTime:    time.Now(),
			DisconnectionTime: time.Now().Add(10 * time.Minute),
		},
	}, 10)
}
