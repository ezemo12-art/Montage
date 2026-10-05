import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';

export const Test: React.FC = () => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const scale = interpolate(spring({frame, fps}), [0, 1], [0.95, 1]);

	return (
		<AbsoluteFill style={{backgroundColor: '#0B0B0F', justifyContent: 'center', alignItems: 'center'}}>
			<div style={{transform: `scale(${scale})`, color: '#FFFFFF', fontSize: 110, fontWeight: 800}}>
				REMOTION <span style={{color: '#FFB800'}}>OK</span>
			</div>
		</AbsoluteFill>
	);
};
