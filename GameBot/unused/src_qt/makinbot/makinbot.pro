#-------------------------------------------------
#
# Project created by QtCreator 2016-06-02T06:35:25
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = makinbot
TEMPLATE = app
LIBS = -lAutoItX3 -L../../lib/

SOURCES += main.cpp\
        mainwindow.cpp\
        ../../src_main/common.c\
        ../../src_main/imageprocess.c\
        ../../src_main/quest.c

HEADERS  += mainwindow.h\
        ../../lib/AutoIt3.h\
        ../../src_main/common.h\
        ../../src_main/imageprocess.h\
        ../../src_main/quest.h


FORMS    += mainwindow.ui
