import pytest, unscammed
from PyQt5 import QtCore


@pytest.fixture
def app(qtbot):
    test_app = unscammed.Main()
    qtbot.addWidget(test_app)
    test_app.show()
    qtbot.wait_for_window_shown(test_app)
    return test_app


def test_Null_IO(app, qtbot):
    main_window = app
    qtbot.mouseClick(main_window.SpamDetectionBTN, QtCore.Qt.LeftButton)
    user_input = ""
    null_input_label = "Please insert a message to verify!"
    app.UserInput.setText(user_input)
    qtbot.mouseClick(main_window.SubmitBTN, QtCore.Qt.LeftButton)
    assert app.WarningLabel.text() == null_input_label


def test_NonNull_IO(app, qtbot):
    main_window = app
    qtbot.mouseClick(main_window.SpamDetectionBTN, QtCore.Qt.LeftButton)
    user_input = "Hello World"
    null_input_label = ""
    app.UserInput.setText(user_input)
    qtbot.mouseClick(main_window.SubmitBTN, QtCore.Qt.LeftButton)
    assert app.WarningLabel.text() == null_input_label
    assert app.CheckedMessage.toPlainText() == user_input


def test_Scam_Result(app, qtbot):
    main_window = app
    qtbot.mouseClick(main_window.SpamDetectionBTN, QtCore.Qt.LeftButton)
    user_input = "Can you send me some bitcoin money please?"
    app.UserInput.setText(user_input)
    qtbot.mouseClick(main_window.SubmitBTN, QtCore.Qt.LeftButton)
    scam_results = '''Check via Naive-Bayes Classification 
Algorithm → Likely a scam

Check via Logistic Regression Classification Algorithm → Likely a scam

Check via Word Count Algorithm → With 60% accuracy, likely a scam'''
    assert app.Results.toPlainText() == scam_results


def test_Ham_Result(app, qtbot):
    main_window = app
    qtbot.mouseClick(main_window.SpamDetectionBTN, QtCore.Qt.LeftButton)
    user_input = "He invited me to a cafe, I'm so excited!"
    app.UserInput.setText(user_input)
    qtbot.mouseClick(main_window.SubmitBTN, QtCore.Qt.LeftButton)
    scam_results = '''Check via Naive-Bayes Classification 
Algorithm → Likely not a scam

Check via Logistic Regression Classification Algorithm → Likely not a scam

Check via Word Count Algorithm → With 95% accuracy, likely not a scam'''
    assert app.Results.toPlainText() == scam_results


def test_Mixed_WC(app, qtbot):
    main_window = app
    qtbot.mouseClick(main_window.SpamDetectionBTN, QtCore.Qt.LeftButton)
    user_input = "dadadad"
    app.UserInput.setText(user_input)
    qtbot.mouseClick(main_window.SubmitBTN, QtCore.Qt.LeftButton)
    scam_results = '''Check via Naive-Bayes Classification 
Algorithm → Likely not a scam

Check via Logistic Regression Classification Algorithm → Likely not a scam

The Word Count Algorithm has detected mixed results'''
    assert app.Results.toPlainText() == scam_results


def test_cleared_all_Backwards(app, qtbot):
    main_window = app
    qtbot.mouseClick(main_window.SpamDetectionBTN, QtCore.Qt.LeftButton)
    user_input = ""
    app.UserInput.setText(user_input)
    qtbot.mouseClick(main_window.SubmitBTN, QtCore.Qt.LeftButton)
    user_input = "Hello"
    app.UserInput.setText(user_input)
    qtbot.mouseClick(main_window.SubmitBTN, QtCore.Qt.LeftButton)
    qtbot.mouseClick(main_window.GoBackBTN_2, QtCore.Qt.LeftButton)
    assert app.WarningLabel.text() == ""
    assert app.UserInput.toPlainText() == ""


def test_cleared_all_Forward(app, qtbot):
    main_window = app
    qtbot.mouseClick(main_window.SpamDetectionBTN, QtCore.Qt.LeftButton)
    user_input = ""
    app.UserInput.setText(user_input)
    qtbot.mouseClick(main_window.SubmitBTN, QtCore.Qt.LeftButton)
    qtbot.mouseClick(main_window.GoBackBTN, QtCore.Qt.LeftButton)
    qtbot.mouseClick(main_window.SpamDetectionBTN, QtCore.Qt.LeftButton)
    assert app.WarningLabel.text() == ""
    assert app.UserInput.toPlainText() == ""
