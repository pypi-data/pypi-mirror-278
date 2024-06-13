import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin,
} from '@jupyterlab/application';
import { ICommandPalette } from '@jupyterlab/apputils';
import { showOnboarding } from './onboarding/showOnboarding';
import { PiecesView } from './ui/piecesView';
import { getStored, setStored } from './localStorageManager';
import { createCommands } from './actions/create_commands';
import * as Sentry from '@sentry/browser';
import { SentryTracking } from './analytics/SentryTracking';
import {
  // ClassificationSpecificEnum,
  ConfigurationParameters,
  // IntentionRequest,
  // SuggestRequest,
} from '@pieces.app/pieces-os-client';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import ConnectorSingleton from './connection/connector_singleton';
import { SegmentAnalytics } from './analytics/SegmentAnalytics';
import { Heartbeat, pluginActivityCheck } from './analytics/Heartbeat';
import { IStateDB } from '@jupyterlab/statedb';
import PiecesCacheSingleton from './cache/pieces_cache';
import { stream } from './connection/stream_assets';
import CheckVersionAndConnection from './connection/checkVersionAndConnection';
import { loadConnect } from './connection/api_wrapper';
import DisplayController from './ui/views/DisplayController';
import versionCheck from './connection/version_check';
import PiecesDB from './models/database_model';
import { returnedSnippet } from './models/typedefs';
import AnnotationHandler from './utils/annotationHandler';
import './globals';
import { ElementMap } from './models/ElementMap';
import ActivitySingleton from './actions/activities';
import { getApplication, initCopilot } from 'copilot/dist/view';
import { copilotParams } from './ui/views/copilot';

/**
 * Initialization data for the jupyter_pieces extension.
 */
export const PLUGIN_ID = 'jupyter_pieces';
export let defaultApp: JupyterFrontEnd;
export let defaultView: PiecesView;
export let theme: string;
export let defaultState: IStateDB;
export let pluginSettings: ISettingRegistry.ISettings;

export const pluginHeartbeat = new Heartbeat(5); // 5 minutes

const plugin: JupyterFrontEndPlugin<void> = {
  id: PLUGIN_ID + ':plugin',
  description:
    'Pieces for Developers is a code snippet management tool powered by AI.',
  autoStart: true,
  requires: [ICommandPalette, IStateDB],
  optional: [],
  deactivate: async () => {
    await Sentry.close(2000);
    pluginHeartbeat.stop();
  },
  activate: async (
    app: JupyterFrontEnd,
    palette: ICommandPalette,
    state: IStateDB
  ) => {
    createPrototypes();
    const cache = PiecesCacheSingleton.getInstance();
    versionCheck({ notify: true }); // Check for minimum version of POS

    theme = '';
    defaultApp = app;
    const piecesView = new PiecesView();
    defaultView = piecesView;
    await piecesView.build(app);
    loadConnect()
      .then((val) => {
        DisplayController.setIsFetchFailed(!val);
        DisplayController.drawSnippets({});
      })
      .catch(() => {
        // do nothing
      });
    createCommands({ palette });

    SentryTracking.init();
    SegmentAnalytics.init();

    pluginHeartbeat.start(() => {
      pluginActivityCheck();
    });

    app.restored
      .then(async () => {
        defaultState = state;
        const data = (await state.fetch(PLUGIN_ID)) as unknown as PiecesDB;
        if (
          !DisplayController.isLoading ||
          //@ts-ignore this is a migration check
          data[0]?.schema ||
          !data.assets[0]?.annotations
        ) {
          return;
        }
        data?.assets?.forEach((val) => (val.created = new Date(val.created)));
        cache.store({
          assets: data.assets as unknown as returnedSnippet[],
        });
        if (data.copilotState) {
          copilotParams.saveState(data.copilotState);
        }
      })
      .finally(async () => {
        CheckVersionAndConnection.run().then(() => {
          AnnotationHandler.getInstance().loadAnnotations().then(stream);
        });
        if (!getStored('onBoardingShown')) {
          showOnboarding();
          setStored({ onBoardingShown: true });
          ActivitySingleton.getInstance().installed();
        }
        initCopilot(copilotParams);
        DisplayController.setIsLoading(false);
        DisplayController.drawSnippets({});
      });

    document.body.addEventListener('click', () => {
      if (theme !== document.body.getAttribute('data-jp-theme-light')) {
        theme = document.body.getAttribute('data-jp-theme-light')!;
        DisplayController.drawSnippets({});
      }
    });

    // TODO reimplement intention and suggestion
    // document.addEventListener('copy', (e) => {
    //   const selection = window.getSelection()?.toString();
    //   if (selection) {
    //     const intention: IntentionRequest = {
    //       application: config.context.application.id,
    //       seededConnectorAsset: {
    //         format: {
    //           fragment: {
    //             string: {
    //               raw: selection,
    //             },
    //             metadata: {
    //               ext: ClassificationSpecificEnum.Py,
    //             },
    //           },
    //         },
    //       },
    //     };
    //     try {
    //       config.api.intention(intention);
    //     } catch (e) {
    //       console.log('Pieces: Intent error', e);
    //     }
    //   }
    // });

    // document.addEventListener('paste', (e) => {
    //   const clipboard = e.clipboardData;
    //   if (clipboard) {
    //     const clipboardData = clipboard.getData('text/plain');
    //     const suggestion: SuggestRequest = {
    //       application: config.context.application.id,
    //       seededConnectorCreation: {
    //         asset: {
    //           format: {
    //             fragment: {
    //               string: {
    //                 raw: clipboardData,
    //               },
    //             },
    //           },
    //         },
    //       },
    //     };
    //     try {
    //       config.api.suggest(suggestion);
    //     } catch (e) {
    //       //
    //     }
    //   }
    // });
  },
};

const createPrototypes = () => {
  /**
   * Array Prototype extensions
   */
  Array.prototype.remove = function <T>(element: T) {
    const idx = this.indexOf(element);
    if (idx === -1) return;
    this.splice(idx, 1);
  };

  /**=
   * HTMLElement Prototype extensions
   */
  HTMLElement.prototype.createEl = function <T extends keyof ElementMap>(
    type: T
  ) {
    const el = document.createElement(type);
    this.appendChild(el);
    return el as ElementMap[T];
  };

  HTMLElement.prototype.createDiv = function (className?: string) {
    const div = document.createElement('div');
    if (className) div.classList.add(className);
    this.appendChild(div);
    return div;
  };

  HTMLElement.prototype.addClass = function (className: string) {
    this.classList.add(className);
  };

  HTMLElement.prototype.addClasses = function (classNames: string[]) {
    for (let i = 0; i < classNames.length; i++) {
      this.classList.add(classNames[i]);
    }
  };

  HTMLElement.prototype.setText = function (text: string) {
    this.innerText = text;
  };

  HTMLElement.prototype.empty = function () {
    this.innerHTML = '';
  };
};

// Getting rid of stupid TS squiggles that aren't actually issues
const settings: JupyterFrontEndPlugin<void> = {
  id: PLUGIN_ID + ':pieces-settings',
  description:
    'Pieces for Developers is a code snippet management tool powered by AI.',
  autoStart: true,
  requires: [ISettingRegistry],
  optional: [],
  activate: async (app: JupyterFrontEnd, settings: ISettingRegistry) => {
    const config: ConnectorSingleton = ConnectorSingleton.getInstance();
    function loadSetting(settings: ISettingRegistry.ISettings): void {
      // Read the settings and convert to the correct type
      if (
        getStored('AutoOpen') !==
        (settings.get('AutoOpen').composite as boolean)
      ) {
        setStored({
          AutoOpen: settings.get('AutoOpen').composite as boolean,
        });
      }

      if (getStored('Port') !== (settings.get('Port').composite as number)) {
        setStored({
          Port: settings.get('Port').composite as number,
        });
        const ConfigParams: ConfigurationParameters = {
          basePath: `http://localhost:${
            settings.get('Port').composite as number
          }`,
          fetchApi: fetch,
        };
        config.parameters = ConfigParams;
      }

      if (
        getStored('Capabilities') !==
        (settings.get('Capabilities').composite as string)
      ) {
        switch (settings.get('Capabilities').composite as string) {
          case 'Local':
            setStored({
              Capabilities: 'Local',
            });
            break;
          case 'Blended':
            setStored({
              Capabilities: 'Blended',
            });
            break;
          case 'Cloud':
            setStored({
              Capabilities: 'Cloud',
            });
            break;
          default:
            setStored({
              Capabilities: 'Blended',
            });
            break;
        }
        getApplication().then((application) => {
          if (!application) return;
          application.capabilities = getStored('Capabilities').toUpperCase();
          copilotParams.updateApplication(application);
        });

        config.application.capabilities =
          getStored('Capabilities').toUpperCase();
      }
    }

    // Wait for the application to be restored and
    // for the settings for this plugin to be loaded
    Promise.all([app.restored, settings.load(PLUGIN_ID + ':pieces-settings')])
      .then(([, settings]) => {
        // Read the settings
        if (settings) {
          pluginSettings = settings;
          loadSetting(settings);
        }

        // Listen for your plugin setting changes using Signal
        settings.changed.connect(loadSetting);
      })
      .catch((reason) => {
        console.error(
          `Something went wrong when reading the settings.\n${reason}`
        );
      });
  },
};

export default [settings, plugin];
