# model: Dueling, agent: rainbow, PER-reward, Update: hard

*general info:*
	game:LunarLander-v2
	seed: 0
	state_size: 8
	action_size: 4

*agent info:*
	Agent: rainbow
	continues: False
	BUFFER_SIZE: 16384
	BATCH_SIZE: 128
	GAMMA: 0.99
	TAU: 0.0001
	LR: 0.001
	UPDATE_MODEL_EVERY: 4
	UPDATE_TARGET_EVERY: 1000
	use_soft_update: False
	priority_method: reward

*per_info:*
	use_per:True
	PER_e: 0.01
	PER_a: 0.6
	PER_b: 0.4
	PER_bi: 0.005
	PER_aeu: 3

*train_info:*
	episodes:400
	max_t: 1000
	eps_start: 1.0
	eps_end: 0.01
	eps_decay: 0.995



## Test data: 

	Episode 100	Average Score: -116.89
	Episode 200	Average Score: -51.07
	Episode 300	Average Score: 9.71
	Episode 400	Average Score: 54.44


best score: 302.24359058862433 at eps: 344

