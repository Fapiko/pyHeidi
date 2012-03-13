#include "qtexteditlinenumber.h"
#include "ui_qtexteditlinenumber.h"

QTextEditLineNumber::QTextEditLineNumber(QWidget *parent) :
    QTextEdit(parent),
    ui(new Ui::QTextEditLineNumber)
{
    ui->setupUi(this);

    connect(this, SIGNAL(blockCountChanged(int)), this, SLOT(updateLineNumberAreaWidth(int)));
    connect(this, SIGNAL(updateRequest(QRect, int)), this, SLOT(updateLineNumberArea(QRect,int)));

    updateLineNumberAreaWidth(0);
}

QTextEditLineNumber::~QTextEditLineNumber()
{
    delete ui;
}

int CodeEditor::lineNumberAreaWidth() {
    int digits = 1;
    int max = qMax(1, blockCount());
    while (max >= 10) {
        max /= 10;
        ++digits;
    }

    int space = 3 + fontMetrics().width(QLatin1Char('9')) * digits;

    return space;
}

void CodeEditor::updateLineNumberAreaWidth(int /* newBlockCount */ ) {
    setViewportMargins(lineNumberAreaWidth(), 0, 0, 0);
}

void CodeEditor::updateLineNumberArea(const QRect &rect, int dy) {
    if (dy)
        ui->lineNumberArea->scroll(0, dy);
    else
        ui->lineNumberArea->update(0, rect.y(), ui->lineNumberArea->width(), rect.height());

    if (rect.contains(viewport()->rect()))
        updateLineNumberAreaWidth(0);
}

void CodeEditor::resizeEvent(QResizeEvent *e) {
     QTextEdit::resizeEvent(e);

     QRect cr = contentsRect();
     ui->lineNumberArea->setGeometry(QRect(cr.left(), cr.top(), lineNumberAreaWidth(), cr.height()));
}

