package usecases

import (
	"mospolytech_app/addiction/models"
	"mospolytech_app/addiction/repositories"
)

type AppUsecase interface {
	PhoneDataProcessing(students []models.AddPhone) error
}

type AppUsecaseImpl struct {
	repositories.AppRepository
}

func NewAppUsecase(repository repositories.AppRepository) *AppUsecaseImpl {
	return &AppUsecaseImpl{
		AppRepository: repository,
	}
}

func (u *AppUsecaseImpl) PhoneDataProcessing(students []models.AddPhone) error {
	if err := u.InsertStudentsData(students); err != nil {
		return err
	}

	return nil
}
