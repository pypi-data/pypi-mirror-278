import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { IThemeManager } from '@jupyterlab/apputils';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { Widget } from '@lumino/widgets';

class UIWidget extends Widget {
  constructor() {
    super();

    setTimeout(function() {
      var bottomBarLeft = document.getElementsByClassName('jp-StatusBar-Left')[0];

      // apply simple UI
      if (bottomBarLeft) {
        const switchElement = bottomBarLeft.getElementsByClassName('jp-switch')[0];

        if (switchElement.getAttribute('aria-checked') === 'false') {
          switchElement?.dispatchEvent(new Event('click'));
        }

        bottomBarLeft?.parentNode?.removeChild(bottomBarLeft);
      }
      
      // remove unwanted elements
      [
        document.getElementsByClassName('jp-StatusBar-Right')[0], // bottom right section
        // document.querySelector('.jp-mod-left [data-id="jp-running-sessions"]'), // elements from the left bar
        // document.querySelector('.jp-mod-left [data-id="table-of-contents"]'), // elements from the left bar
        // document.querySelector('.jp-mod-left [data-id="extensionmanager.main-view"]'), // elements from the left bar
        document.querySelector('.jp-mod-right [data-id="jp-property-inspector"]'), // elements from the left bar
        document.querySelector('.jp-mod-right [data-id="jp-debugger-sidebar"]'), // elements from the left bar
        document.querySelector('#jp-MainLogo svg'), // default logo
        document.querySelector('#jp-title-panel-title'), // default title
      ].forEach((element) => {
        element?.parentNode?.removeChild(element);
      });
      
    }, 500);
  }
}

/**
 * Initialization data for the pergamon_theme extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'pergamon_theme:plugin',
  description: 'Pergamon Theme Extension.',
  autoStart: true,
  requires: [IThemeManager],
  optional: [ISettingRegistry],
  activate: (app: JupyterFrontEnd, manager: IThemeManager, settingRegistry: ISettingRegistry | null) => {
    console.log('JupyterLab extension pergamon_theme is activated!');
    const style = 'pergamon_theme/index.css';

    manager.register({
      name: 'pergamon_theme',
      isLight: true,
      load: () => manager.loadCSS(style),
      unload: () => Promise.resolve(undefined)
    });

    const uiWidget = new UIWidget();
    uiWidget.id = 'PergamonUIWidget';
    app.shell.add(uiWidget, 'bottom');

    if (settingRegistry) {
      settingRegistry
        .load(plugin.id)
        .then(settings => {
          console.log('pergamon_theme settings loaded:', settings.composite);
        })
        .catch(reason => {
          console.error('Failed to load settings for pergamon_theme.', reason);
        });
    }
  }
};

export default plugin;
