from PyQt5.QtWidgets import  QFileDialog

class PlotFile:
    @staticmethod
    def save_plot(figure_save):
        """Сохранение графика."""
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(None, "Save Plot", "", "PNG Files (*.png);;All Files (*)", options=options)
        if fileName:
            figure_save.figure.savefig(fileName)