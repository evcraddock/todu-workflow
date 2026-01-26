# Code Standards

## Formatting

Use rustfmt:

```bash
cargo fmt
```

## Linting

Use clippy:

```bash
cargo clippy
```

Fix all warnings before committing.

## Error Handling

Use `Result` for fallible operations. Avoid `.unwrap()`.

```rust
// ❌ Bad
let file = File::open("config.toml").unwrap();

// ✅ Good
let file = File::open("config.toml")?;

// Or with context
let file = File::open("config.toml")
    .map_err(|e| anyhow!("failed to open config: {}", e))?;
```

### Custom Errors

Use `thiserror` for library errors:

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum UserError {
    #[error("user not found: {0}")]
    NotFound(i64),
    
    #[error("invalid email: {0}")]
    InvalidEmail(String),
}
```

Use `anyhow` for application errors:

```rust
use anyhow::{Context, Result};

fn load_config() -> Result<Config> {
    let contents = fs::read_to_string("config.toml")
        .context("failed to read config file")?;
    
    toml::from_str(&contents)
        .context("failed to parse config")
}
```

## Documentation

Document public items with `///`:

```rust
/// Creates a new user with the given name.
///
/// # Arguments
///
/// * `name` - The user's display name
///
/// # Errors
///
/// Returns an error if the name is empty.
///
/// # Examples
///
/// ```
/// let user = create_user("Alice")?;
/// assert_eq!(user.name, "Alice");
/// ```
pub fn create_user(name: &str) -> Result<User, UserError> {
    // ...
}
```

## Testing

Write tests in the same file:

```rust
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add() {
        assert_eq!(add(2, 3), 5);
    }

    #[test]
    fn test_add_negative() {
        assert_eq!(add(-1, 1), 0);
    }
}
```

### Integration Tests

Put integration tests in `tests/` directory:

```rust
// tests/integration_test.rs
use mylib::create_user;

#[test]
fn test_user_creation() {
    let user = create_user("Alice").unwrap();
    assert_eq!(user.name, "Alice");
}
```

## Imports

Group imports: std, external crates, internal modules.

```rust
use std::collections::HashMap;
use std::fs;

use anyhow::Result;
use serde::Deserialize;

use crate::db::Database;
use crate::models::User;
```
