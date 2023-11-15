# PESDEE-DRAGONFLY-ALGORITHM - Distribution System Planning with Dragonfly Optimization

This repository presents a unique planning methodology for distribution systems, formulated as a nonlinear optimization problem, leveraging the heuristic Dragonfly Optimization Algorithm. Inspired by the swarming behaviors of dragonflies in nature, the algorithm incorporates both exploration and exploitation phases, mimicking the social interactions of dragonflies navigating, searching for food, and avoiding threats.

## Methodology Overview
- **Algorithm Inspiration:** Derived from the static and dynamic swarming behaviors of dragonflies, the Dragonfly Optimization Algorithm is designed for optimization tasks.
- **Integration with OpenDSS and Python:** Utilizes OpenDSS for power flow calculations and Python for data collection, feeder modification, and result visualization.
- **Objective Function:** The Dragonfly Algorithm focuses on reconfiguring the feeder to minimize both expansion costs and technical losses.
- **Testing and Results:** The proposed methodology is tested on the IEEE 123 feeder adapted buses, demonstrating a 22% cost reduction compared to the original expansion plan. The simulation employs 30 dragonflies with a maximum of 25 iterations.

## Article Link
For an in-depth exploration of the methodology and detailed results, please refer to the [article](https://repositorio.ifes.edu.br/bitstream/handle/123456789/1291/TCC_Metodologia_Planejamento_Multiest%C3%A1gios_Expans%C3%A3o_Energia.pdf?sequence=1&isAllowed=y).

## Repository Information
- **GitHub Username:** fernandocalenzani
- **Repository Name:** evolutionary-computing-dragonfly

## How to Access and Contribute
To access the PESDEE-DRAGONFLY-ALGORITHM repository and contribute to its development, follow these steps:
1. **Clone the Repository:** Use the following command to clone the repository to your local machine:
   ```
   git clone https://github.com/fernandocalenzani/evolutionary-computing-dragonfly.git
   ```
2. **Explore and Contribute:** Familiarize yourself with the repository structure and explore opportunities for contribution.
3. **Fork and Pull Request:** Contribute by forking the repository, creating a new branch, implementing changes, and submitting a pull request with a summary of your modifications.

## License
This project is licensed under the [MIT License](LICENSE), allowing for modifications and distribution.

## Acknowledgments
We extend our gratitude to the contributors and researchers involved in the development of the Dragonfly Optimization Algorithm and its application in electric power distribution systems.
