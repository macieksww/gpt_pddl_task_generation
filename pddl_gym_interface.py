import pddlgym
import imageio

env = pddlgym.make("PDDLTiago-v0")
# env = pddlgym.make("PDDLEnvSokoban-v0")
obs, debug_info = env.reset()
print("OBS")
print(obs)
print("DEBUG INFO")
print(debug_info)
print("ACTION SPACE")
print(env.action_space)
# img = env.render()
# imageio.imsave("frame1.png", img)
action = env.action_space.sample(obs)
obs, reward, done, debug_info = env.step(action)
# img = env.render()
# imageio.imsave("frame2.png", img)