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
        .to_string() // return owned String
}

fn parse_line(line: &str) -> (char, i32) {
    let mut chars = line.chars();
    let dir = chars.next().expect("Empty line");
    let num: i32 = chars.as_str().parse().expect("Invalid number");
    (dir, num)
}

fn part1(input: &str) -> i32 {
    let mut position = 50;
    let mut nb_tick_at_zero = 0;

    for line in input.lines() {
        let (direction, number) = parse_line(line);

        position = match direction {
            'L' => (position as i32).wrapping_sub(number) % 100,
            'R' => (position as i32).wrapping_add(number) % 100,
            _ => panic!("Invalid direction: {}", direction),
        };

        if position == 0 {
            nb_tick_at_zero += 1;
        }
    }

    nb_tick_at_zero
}

fn part2(input: &str) -> i32 {
    let mut position = 50;
    let mut nb_tick_at_zero = 0;

    for line in input.lines() {
        let (direction, number) = parse_line(line);

        nb_tick_at_zero += number / 100;

        let is_zero = position == 0;

        position = match direction {
            'L' => position - (number % 100),
            'R' => position + (number % 100),
            _ => panic!("Invalid direction: {}", direction),
        };

        if (position <= 0 && !is_zero) || position > 99 {
            nb_tick_at_zero += 1;
        }
        position = position.rem_euclid(100);
    }

    nb_tick_at_zero
}