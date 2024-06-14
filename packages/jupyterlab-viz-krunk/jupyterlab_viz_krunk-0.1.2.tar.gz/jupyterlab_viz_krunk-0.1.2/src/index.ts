import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

// import { instance } from "@viz-js/viz";

/**
 * Initialization data for the jupyterlab-viz-krunk extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab-viz-krunk:plugin',
  description: 'A JupyterLab extension.',
  autoStart: true,
  activate: (app: JupyterFrontEnd) => {
    console.log('JupyterLab extension jupyterlab-viz-krunk is activated!');
  }
};

export default plugin;
