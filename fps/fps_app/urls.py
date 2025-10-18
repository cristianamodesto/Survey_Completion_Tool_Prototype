from django.urls import path
from . import views

urlpatterns = [
    path('', views.possibleRoutes, name='possibleRoutes'),
    path('selectSurvey/', views.selectSurvey, name='selectSurvey'),
    path('survey/', views.processSelectedSurvey, name='survey'),
    path('login/', views.login, name='login'),
    path('process_login/', views.process_login, name='process_login'),
    path('page/', views.render_surveyFile, name='page'),
    path('loadSurvey/', views.loadSurvey, name='loadSurvey'),
    path('saveSurvey/', views.save_survey, name='saveSurvey'),
    path('updateView/', views.update_view, name='updateView'),
    path('getRecommendations/', views.get_recommendations, name='getRecommendations')
]
