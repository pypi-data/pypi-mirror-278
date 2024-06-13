#!/usr/bin/env python2
"""
A interactive vieweer for gaussian optimization steps
"""

from traits.api import HasTraits, Range, on_trait_change, Instance
from traitsui.api import View, Item, Group
from mayavi.core.api import PipelineBase
from mayavi.core.ui.api import (MayaviScene, SceneEditor,
                                MlabSceneModel)
from mayavi import mlab
from nagausspy import GaussianCom, GaussianLog


class OptViewer(HasTraits):
    """
    A custom viewer based on mayavi to render the diferent frames of a
    Gaussian optimization job. In order to run the viewer, a
    GaussianLog object must be provided in its initialization. Then
    the windows is executed by runing the configure_traits method.

    Parameters
    ----------
    gausslog : GaussianLog
        The gaussianlog object of the job to represent.

    """

    scene = Instance(MlabSceneModel, ())
    plot = Instance(PipelineBase)

    def __init__(self, gausslog, *args, **kwargs):
        super(OptViewer, self).__init__(*args, **kwargs)
        self.ref_log = gausslog
        if isinstance(gausslog, GaussianLog):
            self.add_trait("frame",
                           Range(1, len(self.ref_log.optimization_steps)))
        elif isinstance(gausslog, GaussianCom):
            self.add_trait("frame",
                           Range(1, 1))
        else:
            raise ValueError("Unknown datatype {}".format(type(gausslog)))

    # When the scene is activated, or when the parameters are changed, we
    # update the plot.
    @on_trait_change('frame,scene.activated')
    def update_plot(self):
        """
        Updates the view to the correct frame
        """
        mlab.clf()
        if isinstance(self.ref_log, GaussianLog):
            self.plot = self.ref_log.optimization_steps[self.frame - 1].plot()
        elif isinstance(self.ref_log, GaussianCom):
            self.plot = self.ref_log.geometry.plot()

    # The layout of the dialog created
    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                     height=250, width=300, show_label=False),
                Group('_', 'frame'),
                resizable=True)


if __name__ == "__main__":
    import sys
    from nagausspy import open_file
    VIEWER = OptViewer(open_file(sys.argv[1]))
    VIEWER.configure_traits()
