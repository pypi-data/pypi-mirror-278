from dataclasses import dataclass
from pollination_dsl.dag import Inputs, GroupedDAG, task, Outputs
from pollination.honeybee_display.translate import ModelToVis
from pollination.path.copy import CopyFolder
from pollination.honeybee_radiance.post_process import AbntNbr15575DaylightVisMetadata


@dataclass
class AbntNbr15575DaylightVisualization(GroupedDAG):
    """Create visualization."""

    # inputs
    model = Inputs.file(
        description='Input Honeybee model.',
        extensions=['json', 'hbjson', 'pkl', 'hbpkl', 'zip']
    )

    illuminance_4_930am = Inputs.folder(
        description='Illuminance results for April 23rd 9:30 AM',
        path='simulation/4_930AM/results'
    )

    illuminance_4_330pm = Inputs.folder(
        description='Illuminance results for April 23rd 3:30 PM',
        path='simulation/4_330PM/results'
    )

    illuminance_10_930am = Inputs.folder(
        description='Illuminance results for October 23rd 9:30 AM',
        path='simulation/10_930AM/results'
    )

    illuminance_10_330pm = Inputs.folder(
        description='Illuminance results for October 23rd 3:30 PM',
        path='simulation/10_330PM/results'
    )

    illuminance_levels = Inputs.folder(
        description='Illuminance results for October 23rd 3:30 PM',
        path='visualization/illuminance_levels'
    )

    @task(template=CopyFolder)
    def copy_illuminance_4_930am(self, src=illuminance_4_930am):
        return [
            {
                'from': CopyFolder()._outputs.dst,
                'to': 'visualization/4_930AM'
            }
        ]

    @task(template=CopyFolder)
    def copy_illuminance_4_330pm(self, src=illuminance_4_330pm):
        return [
            {
                'from': CopyFolder()._outputs.dst,
                'to': 'visualization/4_330PM'
            }
        ]

    @task(template=CopyFolder)
    def copy_illuminance_10_930am(self, src=illuminance_10_930am):
        return [
            {
                'from': CopyFolder()._outputs.dst,
                'to': 'visualization/10_930AM'
            }
        ]

    @task(template=CopyFolder)
    def copy_illuminance_10_330pm(self, src=illuminance_10_330pm):
        return [
            {
                'from': CopyFolder()._outputs.dst,
                'to': 'visualization/10_330PM'
            }
        ]

    @task(template=AbntNbr15575DaylightVisMetadata)
    def create_vis_metadata(self, output_folder='visualization'):
        return [
            {
                'from': AbntNbr15575DaylightVisMetadata()._outputs.vis_metadata_folder,
                'to': 'visualization'
            }
        ]

    @task(
        template=ModelToVis,
        needs=[copy_illuminance_4_930am, copy_illuminance_4_330pm,
               copy_illuminance_10_930am, copy_illuminance_10_330pm,
               create_vis_metadata]
    )
    def create_vsf_illuminance(
        self, model=model, grid_data='visualization',
        active_grid_data='4_930AM', output_format='vsf'
    ):
        return [
            {
                'from': ModelToVis()._outputs.output_file,
                'to': 'visualization_illuminance.vsf'
            }
        ]

    @task(template=ModelToVis)
    def create_vsf_illuminance_levels(
        self, model=model, grid_data=illuminance_levels,
        active_grid_data='4_930AM', output_format='vsf'
    ):
        return [
            {
                'from': ModelToVis()._outputs.output_file,
                'to': 'visualization_illuminance_levels.vsf'
            }
        ]

    visualization_illuminance = Outputs.file(
        source='visualization_illuminance.vsf',
        description='Visualization in VisualizationSet format.'
    )

    visualization_illuminance_levels = Outputs.file(
        source='visualization_illuminance_levels.vsf',
        description='Visualization in VisualizationSet format.'
    )
