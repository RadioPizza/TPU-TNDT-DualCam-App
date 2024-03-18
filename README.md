# PTT
Portable thermal testing app

## Сборка приложения
1. Сконвертировать файлы ресурсов .qrc в .py с помощью pyside6-rcc:
- `pyside6-rcc res_rs.qrc -o res_rs.py`   
2. Сконвертировать файлы .ui в файлы .py c помощью pyside6-uic:
- `pyside6-uic MainWindow.ui -o MainWindow.py`
- `pyside6-uic FinishDialog.ui -o FinishDialog.py`
- `pyside6-uic PaleteDialog.ui -o PaleteDialog.py`
- `pyside6-uic PreviewWindow.ui -o PreviewWindow.py`
- `pyside6-uic RetestDialog.ui -o RetestDialog.py`
- `pyside6-uic SettingsWindow.ui -o SettingsWindow.py`
- `pyside6-uic StartDialog.ui -o StartDialog.py`
- `pyside6-uic TrajectoryDialog.ui -o TrajectoryDialog.py`
3. Заменить в этих файлах `import res-rs_rc` на `import res_rs`