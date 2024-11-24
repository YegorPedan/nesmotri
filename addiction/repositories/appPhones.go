package repositories

import (
	"github.com/labstack/gommon/log"
	"mospolytech_app/addiction/models"
	"mospolytech_app/database"
)

type AppRepository interface {
	InsertStudentsData(students []models.AddPhone) error
}

type AppPostgresRepository struct {
	db database.Database
}

func (r *AppPostgresRepository) InsertStudentsData(students []models.AddPhone) error {
	result := r.db.GetDB().Create(&students)

	if result.Error != nil {
		log.Errorf("InsertCockroachData: %v", result.Error)
		return result.Error
	}

	log.Debugf("InsertCockroachData: %v", result.RowsAffected)
	return nil
}
