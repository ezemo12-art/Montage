import {Composition} from 'remotion';
import {Test} from './compositions/Test';

// Format Reels/TikTok/Shorts — voir REGLES_MONTAGE.md §1
export const RemotionRoot: React.FC = () => {
	return (
		<Composition
			id="Test"
			component={Test}
			durationInFrames={60}
			fps={30}
			width={1080}
			height={1920}
		/>
	);
};
