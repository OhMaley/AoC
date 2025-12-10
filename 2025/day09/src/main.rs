use itertools::Itertools;
use std::fs;
use std::path::PathBuf;

fn main() {
    let input = read_input("example.txt");
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

fn parse_input(input: &str) -> Vec<(u32, u32)> {
    let red_tiles_locations: Vec<(u32, u32)> = input
        .lines()
        .map(|line| {
            let mut parts = line.split(',').map(|c| c.parse::<u32>().unwrap());
            let a = parts.next().unwrap();
            let b = parts.next().unwrap();
            (a, b)
        })
        .collect();

    red_tiles_locations
}

fn is_rectangle_inside_shape(shape: &Vec<(u32, u32)>, a: (u32, u32), b: (u32, u32)) -> bool {
    let (x1, y1) = a;
    let (x2, y2) = b;

    let (min_x, max_x) = (x1.min(x2), x1.max(x2));
    let (min_y, max_y) = (y1.min(y2), y1.max(y2));

    for x in min_x..=max_x {
        for y in min_y..=max_y {
            if !is_point_inside_shape(&shape, (x, y)) {
                return false; // rectangle is not fully inside
            }
        }
    }
    return true;
}

fn is_point_inside_shape(shape: &Vec<(u32, u32)>, point: (u32, u32)) -> bool {
    let n = shape.len();
    let mut sign = 0;
    for i in 0..n {
        let (x0, y0) = shape[i];
        let (x1, y1) = shape[(i + 1) % n];
        let cross = (x1 as i64 - x0 as i64) * (point.1 as i64 - y0 as i64)
            - (y1 as i64 - y0 as i64) * (point.0 as i64 - x0 as i64);
        if cross != 0 {
            if sign == 0 {
                sign = cross.signum();
            } else if cross.signum() != sign {
                return false; // outside
            }
        }
        // cross == 0 → point is on the edge; treat as inside
    }
    true
}

fn rectangle_inside_orthogonal_polygon(
    polygon: &Vec<(u32, u32)>,
    rect_corner1: (u32, u32),
    rect_corner2: (u32, u32),
) -> bool {
    if polygon.len() < 4 {
        return false; // Not a valid polygon
    }

    // Determine rectangle bounds
    let (min_x, max_x) = (
        rect_corner1.0.min(rect_corner2.0),
        rect_corner1.0.max(rect_corner2.0),
    );
    let (min_y, max_y) = (
        rect_corner1.1.min(rect_corner2.1),
        rect_corner1.1.max(rect_corner2.1),
    );

    // Convert polygon edges into a set of horizontal and vertical edges for fast checking
    let n = polygon.len();

    for y in min_y..=max_y {
        // Collect all x-intersections at this scanline y
        let mut intersections = Vec::new();
        for i in 0..n {
            let (x0, y0) = polygon[i];
            let (x1, y1) = polygon[(i + 1) % n];

            if y0 == y1 && y0 == y {
                // Horizontal edge lying on the scanline
                intersections.push(x0);
                intersections.push(x1);
            } else if (y0..=y1).contains(&y) || (y1..=y0).contains(&y) {
                // Vertical edge crossing this scanline
                intersections.push(x0);
            }
        }

        intersections.sort_unstable();

        // Check if the rectangle's horizontal segment is fully covered by the polygon at this y
        let mut inside = false;
        let mut coverage_start = 0;
        let mut fully_covered = false;

        let mut it = intersections.iter();
        while let Some(&x) = it.next() {
            if inside {
                let coverage_end = x;
                if coverage_start <= min_x && coverage_end >= max_x {
                    fully_covered = true;
                    break;
                }
                inside = false;
            } else {
                coverage_start = x;
                inside = true;
            }
        }

        if !fully_covered {
            return false; // Rectangle is not fully inside
        }
    }

    true
}

fn part1(input: &str) -> u64 {
    let red_tiles_locations = parse_input(input);

    let largest_area = red_tiles_locations
        .iter()
        .tuple_combinations()
        .map(|(&(x1, y1), &(x2, y2))| {
            let width = (x2 as i64 - x1 as i64).abs() + 1;
            let height = (y2 as i64 - y1 as i64).abs() + 1;
            (width * height) as u64
        })
        .max()
        .unwrap_or(0);

    largest_area
}

fn part2(input: &str) -> u64 {
    let red_tiles_locations = parse_input(input);

    let largest_area = red_tiles_locations
        .iter()
        .tuple_combinations()
        .map(|(a, b)| {
            if rectangle_inside_orthogonal_polygon(&red_tiles_locations, *a, *b) {
                let (x1, y1) = *a;
                let (x2, y2) = *b;
                let width = (x2 as i64 - x1 as i64).abs() + 1;
                let height = (y2 as i64 - y1 as i64).abs() + 1;
                (width * height) as u64
            } else {
                0
            }
        })
        .max()
        .unwrap_or(0);

    largest_area
}
