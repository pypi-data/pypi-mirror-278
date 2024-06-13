# RRIA-API

The `rria-api` is an easy-to-use package that provides a common interface to control robots used by the Residence in Robotics
and AI at the UFPE's informatics center. The API currently supports the use of Kinova Gen3 lite and Niryo NED, with
plans to support a Denso robot.

### **Requirements**

- Python 3.9+
- Kortex API .whl package

### **Installation**
1. Download the v2.3.0 Kortex API .whl package (required for controlling the Kinova Gen3 and Gen3 lite):

   - [kortex_api-2.3.0.post34-py3-none-any.whl](https://artifactory.kinovaapps.com/ui/native/generic-public/kortex/API/2.3.0/kortex_api-2.3.0.post34-py3-none-any.whl).

2. Install the downloaded package with `pip`:

	```
	$ pip install <path to kortex_api-2.3.0.post34-py3-none-any.whl>
	```

3. Install the latest `rria-api` package with `pip`:

	```
	$ pip install rria-api
	```

### **Example**

```python
from rria_api.robot_object import RobotObject
from rria_api.robot_enum import RobotEnum

# Create gen3 RobotObject
gen3_lite = RobotObject('192.168.2.10', RobotEnum.GEN3_LITE)

# Create Niryo NED RobotObject
ned = RobotObject('169.254.200.200', RobotEnum.NED)

gen3_lite.connect_robot()
ned.connect_robot()

gen3_lite.move_joints(30.0, 30.0, 30.0, 30.0, 30.0, 30.0)
ned.move_joints(30.0, 30.0, 30.0, 30.0, 30.0, 30.0)

gen3_lite.get_joints()
ned.get_joints()

gen3_lite.close_gripper()
ned.close_gripper()

gen3_lite.open_gripper()
ned.open_gripper()

gen3_lite.move_to_home()
ned.move_to_home()

gen3_lite.safe_disconnect()
ned.safe_disconnect()

```