use crate::meta_var::{MetaVarEnv, MetaVariable};
use crate::{Doc, Language, Node, Pattern};

use std::borrow::Cow;

fn match_leaf_meta_var<'tree, D: Doc>(
  mv: &MetaVariable,
  candidate: &Node<'tree, D>,
  env: &mut Cow<MetaVarEnv<'tree, D>>,
) -> Option<()> {
  use MetaVariable as MV;
  match mv {
    MV::Capture(name, named) => {
      if *named && !candidate.is_named() {
        None
      } else {
        env.to_mut().insert(name, candidate.clone())?;
        Some(())
      }
    }
    MV::Dropped(named) => {
      if *named && !candidate.is_named() {
        None
      } else {
        Some(())
      }
    }
    // Ellipsis will be matched in parent level
    MV::Multiple => {
      debug_assert!(false, "Ellipsis should be matched in parent level");
      Some(())
    }
    MV::MultiCapture(name) => {
      env.to_mut().insert(name, candidate.clone())?;
      Some(())
    }
  }
}

/// Returns Ok if ellipsis pattern is found. If the ellipsis is named, returns it name.
/// If the ellipsis is unnamed, returns None. If it is not ellipsis node, returns Err.
fn try_get_ellipsis_mode(node: &Pattern<impl Language>) -> Result<Option<String>, ()> {
  let Pattern::MetaVar { meta_var, .. } = node else {
    return Err(());
  };
  match meta_var {
    MetaVariable::Multiple => Ok(None),
    MetaVariable::MultiCapture(n) => Ok(Some(n.into())),
    _ => Err(()),
  }
}

fn match_ellipsis<'t, D: Doc>(
  agg: &mut impl Aggregator<'t, D>,
  optional_name: &Option<String>,
  mut matched: Vec<Node<'t, D>>,
  cand_children: impl Iterator<Item = Node<'t, D>>,
  skipped_anonymous: usize,
) -> Option<()> {
  matched.extend(cand_children);
  agg.match_ellipsis(optional_name.as_deref(), matched, skipped_anonymous)?;
  Some(())
}

struct ComputeEnd(usize);

impl<'t, D: Doc> Aggregator<'t, D> for ComputeEnd {
  fn match_terminal(&mut self, node: &Node<'t, D>) -> Option<()> {
    self.0 = node.range().end;
    Some(())
  }
  fn match_meta_var(&mut self, _: &MetaVariable, node: &Node<'t, D>) -> Option<()> {
    self.0 = node.range().end;
    Some(())
  }
  fn match_ellipsis(
    &mut self,
    _var: Option<&str>,
    nodes: Vec<Node<'t, D>>,
    _skipped: usize,
  ) -> Option<()> {
    let n = nodes.last()?;
    self.0 = n.range().end;
    Some(())
  }
}

pub fn match_end_non_recursive<D: Doc>(
  goal: &Pattern<D::Lang>,
  candidate: Node<D>,
) -> Option<usize> {
  let mut end = ComputeEnd(0);
  match_node_impl(goal, &candidate, &mut end)?;
  Some(end.0)
}

trait Aggregator<'t, D: Doc> {
  fn match_terminal(&mut self, node: &Node<'t, D>) -> Option<()>;
  fn match_meta_var(&mut self, var: &MetaVariable, node: &Node<'t, D>) -> Option<()>;
  fn match_ellipsis(
    &mut self,
    var: Option<&str>,
    nodes: Vec<Node<'t, D>>,
    skipped_anonymous: usize,
  ) -> Option<()>;
}

impl<'t, D: Doc> Aggregator<'t, D> for Cow<'_, MetaVarEnv<'t, D>> {
  fn match_terminal(&mut self, _: &Node<'t, D>) -> Option<()> {
    Some(())
  }
  fn match_meta_var(&mut self, var: &MetaVariable, node: &Node<'t, D>) -> Option<()> {
    match_leaf_meta_var(var, node, self)
  }
  fn match_ellipsis(
    &mut self,
    var: Option<&str>,
    nodes: Vec<Node<'t, D>>,
    skipped_anonymous: usize,
  ) -> Option<()> {
    if let Some(var) = var {
      let mut matched = nodes;
      let skipped = matched.len().saturating_sub(skipped_anonymous);
      drop(matched.drain(skipped..));
      self.to_mut().insert_multi(var, matched)?;
    }
    Some(())
  }
}

fn match_node_impl<'tree, D: Doc>(
  goal: &Pattern<D::Lang>,
  candidate: &Node<'tree, D>,
  agg: &mut impl Aggregator<'tree, D>,
) -> Option<()> {
  use Pattern as P;
  match goal {
    // leaf = without named children
    P::Terminal { text, kind_id, .. } if *kind_id == candidate.kind_id() => {
      if *text == candidate.text() {
        agg.match_terminal(candidate)
      } else {
        None
      }
    }
    P::MetaVar { meta_var, .. } => agg.match_meta_var(meta_var, candidate),
    P::Internal {
      kind_id, children, ..
    } if *kind_id == candidate.kind_id() => {
      let cand_children = candidate.children();
      match_nodes_impl_recursive(children, cand_children, agg)
    }
    _ => None,
  }
}

fn match_nodes_impl_recursive<'tree, D: Doc + 'tree>(
  goals: &[Pattern<D::Lang>],
  candidates: impl Iterator<Item = Node<'tree, D>>,
  agg: &mut impl Aggregator<'tree, D>,
) -> Option<()> {
  let mut goal_children = goals.iter().peekable();
  let mut cand_children = candidates.peekable();
  cand_children.peek()?;
  loop {
    let curr_node = goal_children.peek().unwrap();
    if let Ok(optional_name) = try_get_ellipsis_mode(curr_node) {
      let mut matched = vec![];
      goal_children.next();
      // goal has all matched
      if goal_children.peek().is_none() {
        match_ellipsis(agg, &optional_name, matched, cand_children, 0)?;
        return Some(());
      }
      // skip trivial nodes in goal after ellipsis
      let mut skipped_anonymous = 0;
      while goal_children.peek().unwrap().is_trivial() {
        goal_children.next();
        skipped_anonymous += 1;
        if goal_children.peek().is_none() {
          match_ellipsis(
            agg,
            &optional_name,
            matched,
            cand_children,
            skipped_anonymous,
          )?;
          return Some(());
        }
      }
      // if next node is a Ellipsis, consume one candidate node
      if try_get_ellipsis_mode(goal_children.peek().unwrap()).is_ok() {
        matched.push(cand_children.next().unwrap());
        cand_children.peek()?;
        match_ellipsis(
          agg,
          &optional_name,
          matched,
          std::iter::empty(),
          skipped_anonymous,
        )?;
        continue;
      }
      loop {
        if match_node_impl(
          goal_children.peek().unwrap(),
          cand_children.peek().unwrap(),
          agg,
        )
        .is_some()
        {
          // found match non Ellipsis,
          match_ellipsis(
            agg,
            &optional_name,
            matched,
            std::iter::empty(),
            skipped_anonymous,
          )?;
          break;
        }
        matched.push(cand_children.next().unwrap());
        cand_children.peek()?;
      }
    }
    // skip if cand children is trivial
    loop {
      let Some(cand) = cand_children.peek() else {
        // if cand runs out, remaining goal is not matched
        return None;
      };
      let matched = match_node_impl(goal_children.peek().unwrap(), cand, agg).is_some();
      // try match goal node with candidate node
      if matched {
        break;
      } else if !cand.is_named() {
        // skip trivial node
        // TODO: nade with field should not be skipped
        cand_children.next();
      } else {
        // unmatched significant node
        return None;
      }
    }
    goal_children.next();
    if goal_children.peek().is_none() {
      // all goal found, return
      return Some(());
    }
    cand_children.next();
    cand_children.peek()?;
  }
}

pub fn match_node_non_recursive<'tree, D: Doc>(
  goal: &Pattern<D::Lang>,
  candidate: Node<'tree, D>,
  env: &mut Cow<MetaVarEnv<'tree, D>>,
) -> Option<Node<'tree, D>> {
  match_node_impl(goal, &candidate, env)?;
  Some(candidate)
}

pub fn does_node_match_exactly<D: Doc>(goal: &Node<D>, candidate: &Node<D>) -> bool {
  // return true if goal and candidate are the same node
  if goal.node_id() == candidate.node_id() {
    return true;
  }
  // gh issue #1087, we make pattern matching a little bit more permissive
  // compare node text if at least one node is leaf
  if goal.is_named_leaf() || candidate.is_named_leaf() {
    return goal.text() == candidate.text();
  }
  if goal.kind_id() != candidate.kind_id() {
    return false;
  }
  let goal_children = goal.children();
  let cand_children = candidate.children();
  if goal_children.len() != cand_children.len() {
    return false;
  }
  goal_children
    .zip(cand_children)
    .all(|(g, c)| does_node_match_exactly(&g, &c))
}

pub fn extract_var_from_node<D: Doc>(goal: &Node<D>) -> Option<MetaVariable> {
  let key = goal.text();
  goal.lang().extract_meta_var(&key)
}

#[cfg(test)]
mod test {
  use super::*;
  use crate::language::Tsx;
  use crate::{Root, StrDoc};
  use std::collections::HashMap;

  fn find_node_recursive<'tree>(
    goal: &Pattern<Tsx>,
    node: Node<'tree, StrDoc<Tsx>>,
    env: &mut Cow<MetaVarEnv<'tree, StrDoc<Tsx>>>,
  ) -> Option<Node<'tree, StrDoc<Tsx>>> {
    match_node_non_recursive(goal, node.clone(), env).or_else(|| {
      node
        .children()
        .find_map(|sub| find_node_recursive(goal, sub, env))
    })
  }

  fn test_match(s1: &str, s2: &str) -> HashMap<String, String> {
    let goal = Pattern::new(s1, Tsx);
    let cand = Root::new(s2, Tsx);
    let cand = cand.root();
    let mut env = Cow::Owned(MetaVarEnv::new());
    let ret = find_node_recursive(&goal, cand.clone(), &mut env);
    assert!(
      ret.is_some(),
      "goal: {goal:?}, candidate: {}",
      cand.to_sexp(),
    );
    HashMap::from(env.into_owned())
  }

  fn test_non_match(s1: &str, s2: &str) {
    let goal = Pattern::new(s1, Tsx);
    let cand = Root::new(s2, Tsx);
    let cand = cand.root();
    let mut env = Cow::Owned(MetaVarEnv::new());
    let ret = find_node_recursive(&goal, cand, &mut env);
    assert!(ret.is_none());
  }

  #[test]
  fn test_simple_match() {
    test_match("const a = 123", "const a=123");
    test_non_match("const a = 123", "var a = 123");
  }

  #[test]
  fn test_nested_match() {
    test_match("const a = 123", "function() {const a= 123;}");
    test_match("const a = 123", "class A { constructor() {const a= 123;}}");
    test_match(
      "const a = 123",
      "for (let a of []) while (true) { const a = 123;}",
    );
  }

  #[test]
  fn test_should_exactly_match() {
    test_match(
      "function foo() { let a = 123; }",
      "function foo() { let a = 123; }",
    );
    test_non_match(
      "function foo() { let a = 123; }",
      "function bar() { let a = 123; }",
    );
  }

  #[test]
  fn test_match_inner() {
    test_match(
      "function bar() { let a = 123; }",
      "function foo() { function bar() {let a = 123; }}",
    );
    test_non_match(
      "function foo() { let a = 123; }",
      "function foo() { function bar() {let a = 123; }}",
    );
  }

  #[test]
  fn test_single_ellipsis() {
    test_match("foo($$$)", "foo(a, b, c)");
    test_match("foo($$$)", "foo()");
  }
  #[test]
  fn test_named_ellipsis() {
    test_match("foo($$$A, c)", "foo(a, b, c)");
    test_match("foo($$$A, b, c)", "foo(a, b, c)");
    test_match("foo($$$A, a, b, c)", "foo(a, b, c)");
    test_non_match("foo($$$A, a, b, c)", "foo(b, c)");
  }

  #[test]
  fn test_leading_ellipsis() {
    test_match("foo($$$, c)", "foo(a, b, c)");
    test_match("foo($$$, b, c)", "foo(a, b, c)");
    test_match("foo($$$, a, b, c)", "foo(a, b, c)");
    test_non_match("foo($$$, a, b, c)", "foo(b, c)");
  }
  #[test]
  fn test_trailing_ellipsis() {
    test_match("foo(a, $$$)", "foo(a, b, c)");
    test_match("foo(a, b, $$$)", "foo(a, b, c)");
    // test_match("foo(a, b, c, $$$)", "foo(a, b, c)");
    test_non_match("foo(a, b, c, $$$)", "foo(b, c)");
  }

  #[test]
  fn test_meta_var_named() {
    test_match("return $A", "return 123;");
    test_match("return $_", "return 123;");
    test_non_match("return $A", "return;");
    test_non_match("return $_", "return;");
    test_match("return $$A", "return;");
    test_match("return $$_A", "return;");
  }

  #[test]
  fn test_meta_var_multiple_occurrence() {
    test_match("$A($$$)", "test(123)");
    test_match("$A($B)", "test(123)");
    test_non_match("$A($A)", "test(aaa)");
    test_non_match("$A($A)", "test(123)");
    test_non_match("$A($A, $A)", "test(123, 456)");
    test_match("$A($A)", "test(test)");
    test_non_match("$A($A)", "foo(bar)");
  }

  #[test]
  fn test_string() {
    test_match("'a'", "'a'");
    test_match("'abcdefg'", "'abcdefg'");
    test_match("`abcdefg`", "`abcdefg`");
    test_non_match("'a'", "'b'");
    test_non_match("'abcdefg'", "'gggggg'");
  }

  #[test]
  fn test_skip_trivial_node() {
    test_match("foo($A, $B)", "foo(a, b,)");
    test_match("class A { b() {}}", "class A { get b() {}}");
  }

  #[test]
  fn test_trivia_in_pattern() {
    test_match("foo($A, $B,)", "foo(a, b,)");
    test_non_match("foo($A, $B,)", "foo(a, b)");
    test_match("class A { get b() {}}", "class A { get b() {}}");
    test_non_match("class A { get b() {}}", "class A { b() {}}");
  }

  fn find_end_recursive(goal: &Pattern<Tsx>, node: Node<StrDoc<Tsx>>) -> Option<usize> {
    match_end_non_recursive(goal, node.clone()).or_else(|| {
      node
        .children()
        .find_map(|sub| find_end_recursive(goal, sub))
    })
  }

  fn test_end(s1: &str, s2: &str) -> Option<usize> {
    let goal = Pattern::new(s1, Tsx);
    let cand = Root::new(s2, Tsx);
    let cand = cand.root();
    find_end_recursive(&goal, cand.clone())
  }

  #[test]
  fn test_match_end() {
    let end = test_end("return $A", "return 123 /* trivia */");
    assert_eq!(end.expect("should work"), 10);
    let end = test_end("return f($A)", "return f(1,) /* trivia */");
    assert_eq!(end.expect("should work"), 12);
  }

  // see https://github.com/ast-grep/ast-grep/issues/411
  #[test]
  fn test_ellipsis_end() {
    let end = test_end(
      "import {$$$A, B, $$$C} from 'a'",
      "import {A, B, C} from 'a'",
    );
    assert_eq!(end.expect("must match"), 25);
  }

  #[test]
  fn test_gh_1087() {
    test_match("($P) => $F($P)", "(x) => bar(x)");
  }
}
