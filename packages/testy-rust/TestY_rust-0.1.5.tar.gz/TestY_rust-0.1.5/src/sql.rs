use postgres::{Client, NoTls};
use pyo3::{pyfunction, FromPyObject, PyResult};
use serde::Serialize;
use std::cell::RefCell;
use std::collections::HashMap;
use std::rc::Rc;

type NodeRef = Rc<RefCell<Node>>;

#[derive(Clone)]
struct Node {
    id: i64,
    parent_id: Option<i64>,
    object: TestSuite,
    children: Vec<NodeRef>,
}

trait IntoSuite {
    fn into_suite(self) -> TestSuite;
}

#[derive(Serialize, Clone)]
struct Parent {
    id: i64,
    name: String,
}

#[derive(Clone, Serialize)]
struct TestSuite {
    id: i64,
    parent_id: Option<i64>,
    title: String,
    children: Vec<TestSuite>,
    parent: Option<Parent>,
    test_cases: Vec<TestCase>,
}

#[derive(Serialize, Clone)]
struct TestCase {
    id: i64,
    name: String,
    suite_id: i64,
}

#[derive(FromPyObject)]
pub struct CaseSearchQueryParams {
    suites_query: String,
    cases_query: String,
    host: String,
    user: String,
    password: String,
    dbname: String,
    port: String,
}

impl IntoSuite for NodeRef {
    fn into_suite(self) -> TestSuite {
        let mut self_borrow = self.borrow_mut();
        let mut children = Vec::new();
        for child in self_borrow.children.iter() {
            children.push(child.clone().into_suite())
        }
        self_borrow.object.children = children;
        self_borrow.object.clone()
    }
}

#[pyfunction]
pub fn cases_search(query_params: CaseSearchQueryParams) -> PyResult<String> {
    let host = query_params.host;
    let user = query_params.user;
    let password = query_params.password;
    let dbname = query_params.dbname;
    let port = query_params.port;

    let mut client = Client::connect(
        &format!("host={host} port={port} user={user} password={password} dbname={dbname}"),
        NoTls,
    )
        .expect("Could not establish connection with database");
    let mut suite_map: HashMap<i64, NodeRef> = HashMap::new();
    let mut root_refs = Vec::new();
    for row in client
        .query(&query_params.suites_query, &[])
        .expect("Error occurred in suites query")
    {
        let id: i64 = row.get("id");
        let parent_id = row.get("parent_id");
        let suite = TestSuite {
            id: id,
            parent_id: parent_id,
            title: row.get("title"),
            children: vec![],
            parent: None,
            test_cases: vec![],
        };
        let node = Node {
            id,
            parent_id,
            object: suite,
            children: Vec::new(),
        };
        suite_map.insert(id, Rc::new(RefCell::new(node)));
    }
    for row in client
        .query(&query_params.cases_query, &[])
        .expect("Error occurred in cases query")
    {
        let suite_id: i64 = row.get("suite_id");
        if let Some(node) = suite_map.get(&suite_id) {
            node.borrow_mut().object.test_cases.push(TestCase {
                id: row.get("id"),
                name: row.get("name"),
                suite_id,
            })
        }
    }
    client.close().expect("Could not db close connection");
    for node in suite_map.values() {
        let mut borrowed_node = node.borrow_mut();
        if let Some(parent_id) = borrowed_node.parent_id {
            if let Some(parent) = suite_map.get(&parent_id) {
                let mut borrowed_parent = parent.borrow_mut();
                borrowed_node.object.parent = Option::from(Parent {
                    id: borrowed_parent.id,
                    name: borrowed_parent.object.title.clone(),
                });
                borrowed_parent.children.push(Rc::clone(node));
            }
        } else {
            root_refs.push(Rc::clone(node))
        }
    }

    let mut res: Vec<TestSuite> = Vec::new();
    for elem in root_refs {
        res.push(elem.into_suite());
    }
    Ok(serde_json::to_string(&res).unwrap())
}
