use std::fs;
use std::path::PathBuf;

fn main() {
    let input = read_input("input.txt");
    println!("Solution for part 1: {}", part1(&input));
    println!("Solution for part 2: {}", part2(&input));
}

fn read_input(filename: &str) -> String {
    let mut path = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    path.push(filename);

    fs::read_to_string(path)
        .expect("Could not read the input file")
        .trim()
        .to_string()
}

fn count_accessible_rolls(diagram: &str) -> (i32, Vec<Vec<i32>>) {
    let height = diagram.lines().count();
    let width = diagram.lines().next().map(|l| l.len()).unwrap_or(0);

    let mut grid: Vec<Vec<i32>> = vec![vec![-1; width]; height];

    for (y, line) in diagram.lines().enumerate() {
        for (x, c) in line.chars().enumerate() {
            if c == '@' {
                if grid[y][x] < 0 {
                    grid[y][x] = 0;
                }
                let neighbors = neighbors(diagram, x, y);
                for (nx, ny, nc) in neighbors {
                    if nc == '@' {
                        if grid[ny][nx] < 0 {
                            grid[ny][nx] = 0;
                        }
                        grid[ny][nx] += 1;
                    }
                }
            }
        }
    }

    let count = grid
        .iter()
        .flat_map(|row| row.iter())
        .filter(|&&v| v < 4 && v >= 0)
        .count();

    (count as i32, grid)
}

fn count_accessible_rolls_2(diagram: &str) -> i32 {
    let mut total_accessible_rolls = 0;
    let mut diagram2 = String::from(diagram);

    loop {
        let (accessible_rolls, grid) = count_accessible_rolls(&diagram2);

        if accessible_rolls == 0 {
            break; // exit if nothing left
        }

        total_accessible_rolls += accessible_rolls;
        update_diagram(&mut diagram2, grid);
    }

    total_accessible_rolls
}

fn update_diagram(diagram: &mut String, grid: Vec<Vec<i32>>) {
    let mut lines: Vec<String> = diagram.lines().map(|l| l.to_string()).collect();

    for (y, row) in grid.iter().enumerate() {
        let line = &mut lines[y];
        for (x, &val) in row.iter().enumerate() {
            if val >= 0 && val <= 3 {
                if x < line.len() {
                    line.replace_range(x..x + 1, ".");
                }
            }
        }
    }

    *diagram = lines.join("\n");
}

fn neighbors(grid: &str, x: usize, y: usize) -> Vec<(usize, usize, char)> {
    let lines: Vec<&str> = grid.lines().collect();
    let height = lines.len();
    let width = lines[0].len();

    let mut out = Vec::with_capacity(8);
    let dirs = [
        (-1, -1),
        (0, -1),
        (1, -1),
        (-1, 0),
        (1, 0),
        (-1, 1),
        (0, 1),
        (1, 1),
    ];

    for (dx, dy) in dirs {
        let nx = x as isize + dx;
        let ny = y as isize + dy;

        if nx >= 0 && ny >= 0 && (ny as usize) < height && (nx as usize) < width {
            let row = lines[ny as usize];
            if let Some(ch) = row.chars().nth(nx as usize) {
                out.push((nx as usize, ny as usize, ch));
            }
        }
    }

    out
}

fn part1(input: &str) -> i32 {
    let (nb_accessible_rolls, _grid) = count_accessible_rolls(input);

    nb_accessible_rolls
}

fn part2(input: &str) -> i32 {
    let nb_accessible_rolls = count_accessible_rolls_2(input);

    nb_accessible_rolls
}
