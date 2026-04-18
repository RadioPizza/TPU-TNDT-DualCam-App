# (venv) PS C:\TPU_TNDT_DualCam\TPU-TNDT-DualCam-App> python -m ProcessingWindow.main
if __name__ == '__main__':
    import sys
    from ProcessingWindow import *
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = ProcessingWindow(pipeline=PipelineManager())
    presenter = ProcessingPresenter(window)   # контроллер подключает сигналы
    window.show()
    sys.exit(app.exec())