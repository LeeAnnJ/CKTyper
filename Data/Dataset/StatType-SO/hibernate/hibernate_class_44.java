
//ID = 3853106






public class hibernate_class_44 extends DispatchAction {


	public ActionForward add(ActionMapping mapping, ActionForm form,
			HttpServletRequest request, HttpServletResponse response)
					throws Exception {

		if (log.isDebugEnabled()) {
			log.debug("Entering Master add method");
		}

		try {

			//   cargoForm cargoForm = (cargoForm) form;
			//System.out.println("ID" + cargoForm.getId());
			//   cargo cargo = new cargo();
			//   System.out.println("in cargo Action");
			//   // copy customerform to model
			//   cargoForm.reset(mapping, request);
			//   BeanUtils.copyProperties(cargo, cargoForm);
			//   cargoForm.reset(mapping, request);
			// cargoForm.setInputParam("new");
			// updateFormBean(mapping, request, cargoForm);

		}

		catch (Exception ex) {
			ex.printStackTrace();
			return mapping.findForward("failure");
		}

		return mapping.findForward("success1");
	}

	public ActionForward save(ActionMapping mapping, ActionForm form,
			HttpServletRequest request, HttpServletResponse response)
					throws Exception {

		SessionFactory sessionFactory=null;
		Session session =null;
		System.out.println("in cargo Action");
		try{
			sessionFactory = (SessionFactory) servlet
					.getServletContext().getAttribute("aa");  
			session = sessionFactory.openSession();
			Transaction tx = session.beginTransaction();

			//  cargoForm carForm = (cargoForm) form;


			//  cargo cargo = new cargo();

			System.out.println("in cargo Action");

			//  BeanUtils.copyProperties();
			//  System.out.println("id"+ carForm.getId()); 
			//  System.out.println("item id"+ carForm.getItemid()); 
			//  Set itemset = carForm.getItemDtl();

			//    System.out.println("size"+itemset.size()); 
			////    Iterator iterator =itemset.iterator();   
			//    while(iterator.hasNext()) { 
			////     Item it = (Item)iterator.next();
			//    System.out.println("name"+it.getItemName()); //log.debug("HERE");
			////   it.setCargo(cargo); } 

			//  cargo.setItemList(itemset);
			//  System.out.println("size"+ itemset.size()); 
			//  session.saveOrUpdate("cargo",cargo);
			tx.commit();
		}catch(Exception e){
			e.printStackTrace();
		}
		return mapping.findForward("success");

	}

	public ActionForward search(ActionMapping mapping, ActionForm form,
			HttpServletRequest request, HttpServletResponse response)
					throws Exception {
		System.out.println("in cargo search Action");
		SessionFactory sessionFactory = (SessionFactory) servlet
				.getServletContext().getAttribute("aaa");
		HttpSession session1 = request.getSession();
		Session session = sessionFactory.openSession();
		Transaction tx = session.beginTransaction();
		//  cargoForm cargoform = (cargoForm) form;
		// System.out.println("Name"+cargoForm.getName());
		//  cargo cargo = new cargo();
		System.out.println("in cargo search Action");
		// copy customerform to model
		//  BeanUtils.copyProperties(cargo, cargoform);
		String name = null;
		String status = null;
		String createby = null;


		//  System.out.println("Name..." + name);
		//  System.out.println("status..." + status);
		//  System.out.println("createby..." + createby);
		try {
			//   if ((name.equals("")) && (createby.equals(""))
			//     && (status.equals("")))
			String SQL_QUERY = "createby";
			Query query = session.createQuery(SQL_QUERY);
			query.setParameter("name", name);
			query.setParameter("status", status);
			query.setParameter("createby", createby);
			ArrayList al = new ArrayList();
			for (Iterator i = query.iterate(); i.hasNext();) {
				//    cargo cargo1 = (cargo) i.next();
				//    al.add(cargo1);
				//    System.out.println("Cargo ID is:" + cargo1.getId());
			}
			System.out.println("Cargo list is:" + al.size());
			session1.setAttribute("clist", al);
		} catch (Exception e) {
			e.printStackTrace();
			return mapping.findForward("failure");
		}
		System.out.println("search Cargo list is success");

		return mapping.findForward("success");
	}




	public ActionForward edit(ActionMapping mapping, ActionForm form,
			HttpServletRequest request, HttpServletResponse response)
					throws Exception {
		SessionFactory sessionFactory=null;
		Session session =null;
		if (log.isDebugEnabled()) {
			log.debug("Entering Master Edit method");
		}

		try {
			sessionFactory = (SessionFactory) servlet
					.getServletContext().getAttribute("aa");
			session = sessionFactory.openSession();
			Transaction transaction=session.beginTransaction();
			//   cargoForm carForm = (cargoForm) form;
			// System.out.println(carForm.getStatus());
			// System.out.println(carForm.getCreate());
			//   cargo cargo = new cargo();
			//   BeanUtils.copyProperties(cargo, carForm);
			//      System.out.println("In Cargo Edit "+cargo.getId());
			String qstring = "from cargo c where c.id=:id";
			Query query = session.createQuery(qstring);
			//   query.setParameter("id", cargo.getId());
			ArrayList all = new ArrayList();
			//   cargo c = (cargo) query.iterate().next();

			System.out.println("Edit Cargo list " + all.size()); 


			Set purchaseArray = new HashSet();
			//           System.out.println("Edit"+c.getItemList().size());
			//           carForm.setItemDtl(purchaseArray);
			//           BeanUtils.copyProperties(carForm,c);
			// transaction.commit();
			session.flush();
		} catch (Exception e) {
			e.printStackTrace();
			return mapping.findForward("failure");
		}

		// return a forward to edit forward
		System.out.println("Edit Cargo list is success");
		return mapping.findForward("succ");
	}

	public ActionForward delete(ActionMapping mapping, ActionForm form,
			HttpServletRequest request, HttpServletResponse response)
					throws Exception {

		try {
			SessionFactory sessionFactory = (SessionFactory) servlet
					.getServletContext().getAttribute("aaa");
			Session session = sessionFactory.openSession();
			Transaction tx = session.beginTransaction();
			//   cargoForm carForm = (cargoForm) form;
			// System.out.println(carForm.getStatus());
			// System.out.println(carForm.getCreate());
			//   cargo cargo = new cargo();
			//   BeanUtils.copyProperties(cargo, carForm);
			//      System.out.println("In Cargo Delete "+cargo.getId());
			//   //String qstring = "delete from cargo c where c.id=:id";
			//   //Query query = session.createQuery(qstring);
			//   session.delete("cargo",cargo);
			// session.delete(cargo);
			// session.flush();
			//query.setParameter("id", cargo.getId());
			//int row=query.executeUpdate();
			//System.out.println("deleted row"+row);
			tx.commit();

		} catch (Exception e) {
			e.printStackTrace();
			return mapping.findForward("failure");
		}
		// return a forward to edit forward
		System.out.println("Deleted success");
		return mapping.findForward("succes");
	}

}
