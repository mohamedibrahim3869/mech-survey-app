import json 
import math
import os

class MetalCalculator:
    def __init__(self, materials_path):
        with open(materials_path, 'r') as f:
            self.data = json.load(f)
    def calculate_part_mass(self, length_mm, width_mm, thickness_mm, material_name):
        density = self.data['materials'][material_name]['density_kg_m3']
        volume_m3 = (length_mm * width_mm * thickness_mm) / 1E9
        return volume_m3 * density
    def estimate_sheets_needed(self, total_area_mm2, material_name, sheet_index=0, scrap_factor = 1.15):
        sheet = self.data['materials'][material_name]['standard_sheets'][sheet_index]
        sheet_area_mm2 = sheet['width_mm']  * sheet['length_mm']
        required_area_with_waste = total_area_mm2 * scrap_factor
        num_sheets = math.ceil(required_area_with_waste / sheet_area_mm2)
        return num_sheets, sheet['name']

    def calculate_pipe_mass(self, od_mm, wall_thickness_mm, length_mm, material_name):
        density = self.data['materials'][material_name]['density_kg_m3']
        ro = (od_mm / 2) / 1000
        ri = (od_mm / 2 - wall_thickness_mm) / 1000 
        length_m = length_mm / 1000
        volume_m3 = math.pi * (ro**2 - ri**2) * length_m
        return volume_m3 * density



if __name__ == "__main__" :
    calc = MetalCalculator('src/engine/materials.json')
    mass = calc.calculate_part_mass(1000, 1000, 5, "Mild Steel")
    print(f"Single Plate Mass: {mass:.2f} kg")
