import {Config} from '@remotion/cli/config';
import {existsSync} from 'node:fs';

Config.setVideoImageFormat('jpeg');
Config.setCodec('h264');
Config.setOverwriteOutput(true);

// Environnement cloud : utiliser le Chromium préinstallé (le téléchargement de Remotion y est bloqué).
const localHeadlessShell = '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell';
if (existsSync(localHeadlessShell)) {
	Config.setBrowserExecutable(localHeadlessShell);
}
