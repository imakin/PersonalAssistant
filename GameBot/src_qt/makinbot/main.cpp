#include "mainwindow.h"
#include <QApplication>
#include "windows.h"
#include "../../lib/AutoIt3.h"
#include "../../src_main/quest.h"

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;
    w.show();
    Quest_new(Quest);
    Quest->next_node(Quest);

    AU3_MouseMove(40,40,10);

    return a.exec();
}
