use std::collections::BTreeMap;
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

fn find_maximum_joltage_in_bank(bank: &str) -> i32 {
    let mut max_thenth_char = '0';
    let mut max_unit_char = '0';

    let chars: Vec<_> = bank.chars().collect();
    for i in 0..chars.len() - 1 {
        let c1 = chars[i];
        if c1 > max_thenth_char {
            max_thenth_char = c1;
            max_unit_char = '0';
        }
        for j in i + 1..chars.len() {
            let c2 = chars[j];
            if c2 > max_unit_char {
                max_unit_char = c2;
            }
        }
    }

    let tenth_digit = max_thenth_char.to_digit(10).unwrap();
    let unit_digit = max_unit_char.to_digit(10).unwrap();
    let maximum_joltage = (tenth_digit * 10 + unit_digit) as i32;

    maximum_joltage
}

fn find_maximum_joltage_in_bank_v2(bank: &str, nb_max_batteries: u8) -> i64 {
    // Map the positions of each digit in the bank
    let mut digits_position_map: BTreeMap<char, Vec<u8>> =
        ('1'..='9').map(|c| (c, Vec::new())).collect();

    for (i, c) in bank.char_indices() {
        digits_position_map.get_mut(&c).unwrap().push(i as u8);
    }

    // Pick the first highest digit available
    let bank_length = bank.len() as u8;
    let mut lower_index = 0;
    let mut higher_index = bank_length - nb_max_batteries;

    let mut highest_number = String::new();
    for _i in 0..=nb_max_batteries - 1 {
        let result =
            find_biggest_key_with_value_in_range(&digits_position_map, lower_index, higher_index);
        let (digit, index) = result.unwrap();
        highest_number.push(digit);

        lower_index = index + 1;
        higher_index += 1;
    }

    let maximum_joltage: i64 = highest_number.parse::<i64>().unwrap();

    maximum_joltage
}

fn find_biggest_key_with_value_in_range(
    map: &BTreeMap<char, Vec<u8>>,
    lower_index: u8,
    higher_index: u8,
) -> Option<(char, u8)> {
    for (&key, values) in map.iter().rev() {
        // Find all values within range
        let mut matches: Vec<u8> = values
            .iter()
            .copied()
            .filter(|v| *v >= lower_index && *v <= higher_index)
            .collect();

        // Select the smallest index
        if !matches.is_empty() {
            matches.sort(); // sort ascending
            let smallest = matches[0]; // smallest matching value
            return Some((key, smallest));
        }
    }

    None
}

fn part1(input: &str) -> i32 {
    let mut total_output_joltage: i32 = 0;

    for line in input.lines() {
        let maximum_joltage = find_maximum_joltage_in_bank(line);
        total_output_joltage += maximum_joltage;
    }

    total_output_joltage
}

fn part2(input: &str) -> i64 {
    let mut total_output_joltage: i64 = 0;

    for line in input.lines() {
        let maximum_joltage = find_maximum_joltage_in_bank_v2(line, 12);
        total_output_joltage += maximum_joltage;
    }

    total_output_joltage
}
