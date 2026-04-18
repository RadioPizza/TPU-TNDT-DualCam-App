# (venv) PS C:\TPU_TNDT_DualCam\TPU-TNDT-DualCam-App> python -m Processing.main
if __name__ == '__main__':
    import sys
    from Processing import *
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = ProcessingWindow(pipeline=PipelineManager())
    presenter = ProcessingPresenter(window)
    window.show()
    sys.exit(app.exec())