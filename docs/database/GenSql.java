package util;

import java.io.File;
import java.sql.Connection;
import java.sql.DatabaseMetaData;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

import org.apache.commons.io.FileUtils;
import org.apache.commons.lang3.StringUtils;
import org.springframework.jdbc.support.JdbcUtils;

public class GenSql {
	
	String SCHEMA_NAME	= "US_RIMSOWNDEV";
	String DRIVER_NAME	= "oracle.jdbc.driver.OracleDriver";
	String JDBC_URL		= "jdbc:oracle:thin:@192.168.200.111:1521/RIMSPINT";  // 서비스명으로 접근. sid 아님. 
	String USER			= "US_RIMSAPPDEV";
	String PWD			= "US_RIMSAPPDEV";
	
	String outPath = "C:/eGovFrameDev-3.7.0-32bit/workspace/RIMS/src/main/resources/sqlmap/exe";
	
	String[] tableNames = {

			 "TEXE0110"
			,"TEXE0111"
			,"TEXE0112"
			/*
			 "TEXE0101"
			,"TEXE0102"
			,"TEXE0103"
			,"TEXE0104"
			,"TEXE0105"
			,"TEXE0106"
			,"TEXE0107"
			,"TEXE0108"
			,"TEXE0109"
			,"TEXE0110"
			,"TEXE0111"
			,"TEXE0112"
			,"TEXE0113"
			,"TEXE0114"
			,"TEXE0115"
			,"TEXE0116"
			,"TEXE0117"
			,"TEXE0118"
			,"TEXE0201"
			,"TEXE0202"
			,"TEXE0205"
			,"TEXE0206"
			,"TEXE0207"
			,"TEXE0208"
			,"TEXE0209"
			,"TEXE0210"
			,"TEXE0211"
			,"TEXE0212"
			,"TEXE0213"
			,"TEXE0214"
			,"TEXE0301"
			,"TEXE0302"
			,"TEXE0303"
			,"TEXE0306"
			,"TEXE0308"
			,"TEXE0309"		
			*/
	};
//	idx 0: 시퀀스가 있는 테이블명, idx 1:시퀀스가 있는 pk index(base 0)
	String[][] seqTables = {
			 {"TEXE0101","0"} // 이체내역
			,{"TEXE0102","0"} // 사용내역
			,{"TEXE0104","1"} // 참석자
			,{"TEXE0105","1"} // 품목상세
			,{"TEXE0107","0"} // 일괄집행
			,{"TEXE0108","1"} // 이체전문송신내역
			,{"TEXE0109","0"} // 환입계획
			,{"TEXE0201","1"}
			,{"TEXE0208","1"}
			,{"TEXE0301","1"}
			,{"TEXE0302","1"}
			,{"TEXE0303","1"}
			,{"TEXE0306","2"}
			,{"TEXE0309","1"}	
	};
	
	public GenSql() throws Exception {
		// TODO Auto-generated method stub
		
        Class.forName(DRIVER_NAME);
        Connection con = DriverManager.getConnection(JDBC_URL,USER,PWD);

        for (String tableName : tableNames) {
        	
            PreparedStatement ps = con.prepareStatement("SELECT * FROM "+tableName+" WHERE 1=0");
            System.out.println(tableName +" 테이블 쿼리 생성 시작");
            ResultSet rs = ps.executeQuery();
            ResultSetMetaData md = rs.getMetaData();

			List<FieldVo> pkList = getPKList(con, tableName);
			
	        StringBuffer dml = new StringBuffer();		
	        
			dml.append(getSqlMapHeader(tableName));

	        dml.append(getInsertClause(pkList, tableName));
	        dml.append(getInsertFieldClause(md));
	        dml.append(getInsertValueClause(md));
			dml.append("\t").append("</insert>").append("\n");
						
	        dml.append(getSelectClause(tableName));
	        dml.append(getSelectFieldClause(md));
	        dml.append(getSelectConditionClause(tableName, md, pkList));
			dml.append("\t").append("</select>").append("\n");
			
	        dml.append(getUpdateClause(tableName));
	        dml.append(getUpdateFieldClause(md));
	        dml.append(getUpdateConditionClause(tableName, md, pkList));
			dml.append("\t").append("</update>").append("\n");
			
	        dml.append("\n").append("</mapper>").append("\n");
			
			File file = new File(outPath+"/"+tableName+"_00_DAO.xml");
			FileUtils.write(file, dml);
			
	        rs.close();
	        ps.close();
        }
        
        con.close();
	}
	private List<FieldVo> getPKList(Connection con, String tableName) throws Exception {
			
    	DatabaseMetaData dbmd = con.getMetaData();
    	ResultSet pkCols = dbmd.getPrimaryKeys(null, SCHEMA_NAME, tableName);

		List<FieldVo> list = new ArrayList<FieldVo>();
        while (pkCols.next()) {
        	
        	String colName = pkCols.getString("COLUMN_NAME");
        	int keySeq = pkCols.getInt("KEY_SEQ");
        	
        	FieldVo vo = new FieldVo(keySeq, colName);
        	list.add(vo);
        }
        Collections.sort(list);
        
        return list;
	}
	
	private StringBuffer getSqlMapHeader(String tableName) {
		
		StringBuffer dml = new StringBuffer();
		
		dml.append("<?xml version=\"1.0\" encoding=\"UTF-8\"?>").append("\n");
		dml.append("<!DOCTYPE mapper PUBLIC \"-//mybatis.org//DTD Mapper 3.0//EN\" \"http://mybatis.org/dtd/mybatis-3-mapper.dtd\"> ").append("\n");
		dml.append("<mapper namespace=\"").append(tableName).append("_00_DAO\">").append("\n");
        dml.append("\n");
        
        return dml;
	}
	
	private StringBuffer getInsertClause(List<FieldVo> pkList, String tableName) throws Exception {
		
		StringBuffer dml = new StringBuffer();
		
		dml.append("\t").append("<insert id=\"").append(tableName).append("_00_DAO_insert\" parameterType=\"rims.ezbaro.exe.vo.ExeVO\">  ").append("\n");	
		
		int seqTableIdx = getOracleSeqIdx(tableName);
		
		if (seqTableIdx >= 0) {
			// base 0
			int seqIdx = Integer.parseInt(seqTables[seqTableIdx][1]);
			System.out.println(seqTableIdx);
			System.out.println(seqTables[seqTableIdx][1]);
			FieldVo pkField = pkList.get(seqIdx);
			String seqPkName = pkField.getColName();
			dml.append(buildSeqKeyClause(seqPkName, tableName));
		}
		dml.append("\t\t").append("INSERT INTO ").append(tableName).append("\n");
		
		return dml;
	}
	
	private int getOracleSeqIdx(String tableName) {
		
		for (int i=0; i<seqTables.length; i++) {
			String seqTbl = seqTables[i][0];
			if (StringUtils.equals(tableName, seqTbl)) {
				return i;
			}
		}
		return -1;
	}
	
	private StringBuffer buildSeqKeyClause(String pk1, String tableName) throws Exception {
		
		StringBuffer dml = new StringBuffer();
		
		String seqPrefix = "S"+StringUtils.substring(tableName, 1);
		String pkFieldName = JdbcUtils.convertUnderscoreNameToPropertyName(pk1);
		dml.append("\t\t").append("<selectKey keyProperty=\"").append(pkFieldName).append("\" resultType=\"string\" order=\"BEFORE\">").append("\n");	
		dml.append("\t\t\tSELECT ").append(seqPrefix).append("_01.NEXTVAL FROM DUAL").append("\n");
		dml.append("\t\t</selectKey>").append("\n");
		
		return dml;
	}
	
	private StringBuffer getInsertFieldClause(ResultSetMetaData md) throws Exception {
		
		StringBuffer dml = new StringBuffer();

		dml.append("\t\t").append("(").append("\n");
		
        int colCnt = md.getColumnCount();        
        for (int i=0; i<colCnt; i++) {
        	int colIdx = i+1;

        	String name = md.getColumnName(colIdx);

    		if (i==0) {
    			dml.append("\t\t\t").append(name).append("\n");
    		} else {
    			dml.append("\t\t\t").append(", ").append(name).append("\n");
    		}    		
        }
        dml.append("\t\t").append(")").append("\n");
        
        return dml;
	}
	
	private StringBuffer getInsertValueClause(ResultSetMetaData md) throws Exception {
		
		StringBuffer dml = new StringBuffer();

		dml.append("\t\t").append("VALUES").append("\n");
		dml.append("\t\t").append("(").append("\n");
		
        int colCnt = md.getColumnCount();        
        for (int i=0; i<colCnt; i++) {
        	int colIdx = i+1;
        	/*
        	int type = md.getColumnType(colIdx);
        	String typeName = md.getColumnTypeName(colIdx);
        	String label = md.getColumnLabel(colIdx);
        	String className = md.getColumnClassName(colIdx);
        	*/

        	String colName = md.getColumnName(colIdx);
        	String typeName = md.getColumnTypeName(colIdx);
        	String fieldName = JdbcUtils.convertUnderscoreNameToPropertyName(colName);
        	if (StringUtils.equals(typeName, "DATE")) {
        		fieldName = "SYSDATE";
        		dml.append("\t\t\t").append(", ").append(fieldName).append("\n");
        		continue;
        	}

    		if (i==0) {
    			dml.append("\t\t\t").append(" #{").append(fieldName).append("}").append("\n");
    		} else {
    			dml.append("\t\t\t").append(", #{").append(fieldName).append("}").append("\n");
    		}    
        }
		dml.append("\t\t").append(")").append("\n");
		
        return dml;
	}
	
	private StringBuffer getSelectClause(String tableName) throws Exception {
		
		StringBuffer dml = new StringBuffer();
		dml.append("\t").append("<select id=\"").append(tableName).append("_00_DAO_select\" parameterType=\"rims.ezbaro.exe.vo.ExeSearchVO\" resultType=\"egovMap\">").append("\n");
		dml.append("\t\t").append("SELECT	/* ").append(tableName).append("_00_DAO_select */").append("\n");
		return dml;
	}
	
	private StringBuffer getSelectFieldClause(ResultSetMetaData md) throws Exception {
		
		StringBuffer dml = new StringBuffer();
		
        int colCnt = md.getColumnCount();        
        for (int i=0; i<colCnt; i++) {
        	int colIdx = i+1;

        	String name = md.getColumnName(colIdx);

    		if (i==0) {
    			dml.append("\t\t\t").append(name).append("\n");
    		} else {
    			dml.append("\t\t\t").append(", ").append(name).append("\n");
    		}    		
        }
        
        return dml;
	}
	
	private StringBuffer getSelectConditionClause(String tableName, ResultSetMetaData md, List<FieldVo> pkList) throws Exception {
		
		StringBuffer dml = new StringBuffer();		
		dml.append("\t\t").append("FROM  ").append(tableName).append("\n")
			.append("\t\t").append("WHERE").append("\n");
        
        for (int i=0; i<pkList.size(); i++) {
        	
        	FieldVo vo = pkList.get(i);
        	String fieldName = JdbcUtils.convertUnderscoreNameToPropertyName(vo.getColName());
//    		PK1 이면 
    		if (i==0) {
    			dml.append("\t\t\t\t").append(vo.getColName()).append("\t").append("=").append(" #{").append(fieldName).append("}").append("\n");
    		} else {
    			dml.append("\t\t\t").append("AND ").append(vo.getColName()).append("\t").append("=").append(" #{").append(fieldName).append("}").append("\n");
    		} 
        }
		
        return dml;
	}
	
	private StringBuffer getUpdateClause(String tableName) throws Exception {
				
		StringBuffer dml = new StringBuffer();
		dml.append("\t").append("<update id=\"").append(tableName).append("_00_DAO_update\" parameterType=\"rims.ezbaro.exe.vo.ExeVO\">").append("\n");
		dml.append("\t\t").append("UPDATE	").append(tableName).append("\t/* ").append(tableName).append("_00_DAO_update */").append("\n");
		dml.append("\t\t").append("SET").append("\n");
		
		return dml;
	}
	
	private StringBuffer getUpdateFieldClause(ResultSetMetaData md) throws Exception {
		
		StringBuffer dml = new StringBuffer();
		
        int colCnt = md.getColumnCount();        
        for (int i=0; i<colCnt; i++) {
        	int colIdx = i+1;

        	String colName = md.getColumnName(colIdx);
        	String typeName = md.getColumnTypeName(colIdx);
        	
        	if (StringUtils.equals(colName, "RG_GUID")
        			|| StringUtils.equals(colName, "REGISTER_ID")
        			|| StringUtils.equals(colName, "RG_DT")) {
        		continue;
        	}
        	
        	if (StringUtils.equals(colName, "ALT_DT")) {
        		
        		dml.append(String.format("\t\t\t\t%-20s = SYSDATE\n", ","+colName));
        		continue;
        	}

        	String fieldName = JdbcUtils.convertUnderscoreNameToPropertyName(colName);
        	String line = "";
    		
    		if (StringUtils.contains(typeName, "NUMBER")) {
    			line = String.format("\t\t\t\t%-20s = DECODE(#{%s},0, %s, #{%s})\n", ((i>0)?","+colName:colName),fieldName,colName,fieldName);    			
    		} else {
    			line = String.format("\t\t\t\t%-20s = NVL(#{%s}, %s)\n", ((i>0)?","+colName:colName),fieldName,colName);
    		} 
    		dml.append(line);
        }
        
        return dml;
	}
	
	private StringBuffer getUpdateConditionClause(String tableName, ResultSetMetaData md, List<FieldVo> pkList) throws Exception {
		
		StringBuffer dml = new StringBuffer();		
		dml.append("\t\t").append("WHERE").append("\n");
        
        for (int i=0; i<pkList.size(); i++) {
        	
        	FieldVo vo = pkList.get(i);
        	String fieldName = JdbcUtils.convertUnderscoreNameToPropertyName(vo.getColName());
//    		PK1 이면 
    		if (i==0) {
    			dml.append("\t\t\t\t").append(vo.getColName()).append("\t\t\t").append("=").append(" #{").append(fieldName).append("}").append("\n");
    		} else {
    			dml.append("\t\t\t").append("AND ").append(vo.getColName()).append("\t\t\t").append("=").append(" #{").append(fieldName).append("}").append("\n");
    		} 
        }
		
        return dml;
	}
	
	public static void main(String[] args) throws Exception {
		
		new GenSql();
	}
}
