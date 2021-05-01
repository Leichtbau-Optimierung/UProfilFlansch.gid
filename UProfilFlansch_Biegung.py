import sys
import time

import KratosMultiphysics
from KratosMultiphysics.StructuralMechanicsApplication.structural_mechanics_analysis import StructuralMechanicsAnalysis
try:
    from KratosTools.KratosVisualization import VisualizeMesh, VisualizeNodalResults
    KratosToolsPresent = True
except:
    KratosToolsPresent = False

class StructuralMechanicsAnalysisWithFlush(StructuralMechanicsAnalysis):

    def __init__(self, model, project_parameters, flush_frequency=10.0):
        super().__init__(model, project_parameters)
        self.flush_frequency = flush_frequency
        self.last_flush = time.time()
        sys.stdout.flush()

    def Initialize(self):
        super().Initialize()
        sys.stdout.flush()

    def FinalizeSolutionStep(self):
        super().FinalizeSolutionStep()

        if self.parallel_type == "OpenMP":
            now = time.time()
            if now - self.last_flush > self.flush_frequency:
                sys.stdout.flush()
                self.last_flush = now


with open("ProjectParameters.json", 'r') as parameter_file:
    parameters = KratosMultiphysics.Parameters(parameter_file.read())

global_model = KratosMultiphysics.Model()
simulation = StructuralMechanicsAnalysisWithFlush(global_model, parameters)
simulation.Run()

# Post-processing
if KratosToolsPresent:
    meshFig = VisualizeMesh()
    meshFig.vtkFolder = "vtk_output"
    meshFig.vtkFile = "Structure_0_1.vtk"
    meshFig.name = "UProfilFlansch"
    meshFig.view =  (0.5, -0.5, 0.5)
    meshFig.make()
    NodalFig = VisualizeNodalResults()
    NodalFig.name = "UProfilFlansch"
    NodalFig.vtkFolder = "vtk_output"
    NodalFig.vtkFile = "Structure_0_1.vtk"
    NodalFig.showNodes = False
    NodalFig.showMesh = True
    NodalFig.showColorBar = False
    NodalFig.Factor = 1
    NodalFig.view =  (0.5, -0.5, 0.5)
    NodalFig.Responses = ["DISPLACEMENT"]
    NodalFig.FileNameAdd = ["Displacement"]
    NodalFig.BarTitles = ["|deformation| [mm]"]
    NodalFig.make()
