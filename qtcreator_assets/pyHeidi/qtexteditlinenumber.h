#ifndef QTEXTEDITLINENUMBER_H
#define QTEXTEDITLINENUMBER_H

#include <QWidget>
#include <QTextEdit>

namespace Ui {
    class QTextEditLineNumber;
}

class QTextEditLineNumber : public QTextEdit
{
    Q_OBJECT
    
public:
    explicit QTextEditLineNumber(QTextEdit *parent = 0);
    ~QTextEditLineNumber();

    void lineNumberAreaPaintEvent(QPaintEvent *event);
    int lineNumberAreaWidth();

protected:
    void resizeEvent(QResizeEvent *event);
    
private slots:
    void updateLineNumberAreaWidth(int newBlockCount);
    void updateLineNumberArea(const QRect &, int);

private:
    Ui::QTextEditLineNumber *ui;
};

#endif // QTEXTEDITLINENUMBER_H
